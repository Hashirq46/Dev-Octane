from django.contrib import messages
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect, render
from accounts.decorators import candidate_required
from parsing.models import ParsedDraft
from parsing.tasks import enqueue
from .forms import (
    CandidateProfileEditForm,
    CandidateReviewForm,
    EducationForm,
    ExperienceForm,
)
from .models import CandidateProfile, Education, WorkExperience

EducationFS = formset_factory(EducationForm, extra=1, can_delete=True)
ExperienceFS = formset_factory(ExperienceForm, extra=1, can_delete=True)


def _rows(fs):
    for f in fs.cleaned_data:
        if f and not f.get('DELETE'):
            row = {k: v for k, v in f.items() if k != 'DELETE'}
            if any(str(v).strip() for v in row.values()):
                yield row


@candidate_required
def review_cv(request, draft_id):
    draft = get_object_or_404(ParsedDraft, pk=draft_id, user=request.user, kind='cv')
    if draft.state == 'submitted':
        return redirect('candidate_dashboard')
    if draft.state == 'pending':
        return render(request, 'candidates/processing.html', {'draft': draft})

    d = draft.data or {}
    if request.method == 'POST':
        form = CandidateReviewForm(request.POST)
        edu = EducationFS(request.POST, prefix='edu')
        exp = ExperienceFS(request.POST, prefix='exp')
        if form.is_valid() and edu.is_valid() and exp.is_valid():
            p, _ = CandidateProfile.objects.get_or_create(
                user=request.user,
                defaults={'full_name': form.cleaned_data.get('full_name') or request.user.get_full_name()}
            )
            for f in ('full_name', 'phone', 'city', 'headline', 'skills', 'experience_years'):
                setattr(p, f, form.cleaned_data[f])
            if draft.file:
                p.resume = draft.file.name
            p.save()

            p.education.all().delete()
            p.experience.all().delete()
            for row in _rows(edu):
                Education.objects.create(profile=p, **row)
            for row in _rows(exp):
                WorkExperience.objects.create(profile=p, **row)

            draft.state = 'submitted'
            draft.save()
            messages.success(request, 'Your profile has been saved successfully!')
            return redirect('candidate_dashboard')
    else:
        skills_raw = d.get('skills', [])
        if isinstance(skills_raw, list):
            skills_val = ', '.join(skills_raw)
        else:
            skills_val = str(skills_raw)

        initial_data = {
            'full_name': d.get('full_name') or getattr(getattr(request.user, 'candidate_profile', None), 'full_name', ''),
            'phone': d.get('phone', ''),
            'city': d.get('city', ''),
            'headline': d.get('headline', ''),
            'skills': skills_val,
            'experience_years': d.get('experience_years', 0),
        }
        form = CandidateReviewForm(initial=initial_data)
        edu = EducationFS(initial=d.get('education', []), prefix='edu')
        exp = ExperienceFS(initial=d.get('experience', []), prefix='exp')

    return render(
        request,
        'candidates/review_cv.html',
        {
            'draft': draft,
            'form': form,
            'edu': edu,
            'exp': exp,
            'failed': draft.state == 'failed',
        }
    )


@candidate_required
def candidate_dashboard(request):
    profile, _ = CandidateProfile.objects.get_or_create(
        user=request.user,
        defaults={'full_name': request.user.username}
    )
    applications = request.user.applications.select_related('job', 'job__recruiter').order_by('-applied_at')
    unsubmitted_draft = (
        ParsedDraft.objects.filter(user=request.user, kind='cv')
        .exclude(state='submitted')
        .order_by('-created_at')
        .first()
    )

    return render(
        request,
        'candidates/dashboard.html',
        {
            'profile': profile,
            'applications': applications,
            'unsubmitted_draft': unsubmitted_draft,
            'completeness': profile.completeness_percentage,
        }
    )


@candidate_required
def edit_profile(request):
    profile, _ = CandidateProfile.objects.get_or_create(
        user=request.user,
        defaults={'full_name': request.user.username}
    )

    if request.method == 'POST':
        form = CandidateProfileEditForm(request.POST, request.FILES, instance=profile)
        edu = EducationFS(request.POST, prefix='edu')
        exp = ExperienceFS(request.POST, prefix='exp')
        if form.is_valid() and edu.is_valid() and exp.is_valid():
            new_cv = form.cleaned_data.get('new_cv')
            if new_cv:
                # Trigger a new draft and review flow
                draft = ParsedDraft.objects.create(
                    user=request.user,
                    kind='cv',
                    label='cv',
                    file=new_cv
                )
                enqueue(draft.id)
                messages.info(request, 'New CV uploaded. Processing with AI for review...')
                return redirect('review_cv', draft_id=draft.id)

            form.save()
            profile.education.all().delete()
            profile.experience.all().delete()
            for row in _rows(edu):
                Education.objects.create(profile=profile, **row)
            for row in _rows(exp):
                WorkExperience.objects.create(profile=profile, **row)
            messages.success(request, 'Profile updated successfully.')
            return redirect('candidate_dashboard')
    else:
        form = CandidateProfileEditForm(instance=profile)
        edu_data = [{'degree': e.degree, 'institute': e.institute, 'year': e.year} for e in profile.education.all()]
        exp_data = [
            {'title': x.title, 'company': x.company, 'start': x.start, 'end': x.end, 'description': x.description}
            for x in profile.experience.all()
        ]
        edu = EducationFS(initial=edu_data, prefix='edu')
        exp = ExperienceFS(initial=exp_data, prefix='exp')

    return render(
        request,
        'candidates/edit_profile.html',
        {
            'form': form,
            'edu': edu,
            'exp': exp,
            'profile': profile,
        }
    )
