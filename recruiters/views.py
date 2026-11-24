from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from accounts.decorators import recruiter_required
from jobs.models import Application, Job
from parsing.models import ParsedDraft
from parsing.tasks import enqueue
from .forms import CompanyDocsForm, VerificationForm
from .models import RecruiterVerification
from .services import check_atl, company_flags, merged_company_data


@recruiter_required
def recruiter_dashboard(request):
    verification = RecruiterVerification.objects.filter(user=request.user).first()
    my_jobs = Job.objects.filter(recruiter=request.user)
    total_jobs = my_jobs.count()
    active_jobs = my_jobs.filter(is_active=True).count()
    total_applicants = Application.objects.filter(job__recruiter=request.user).count()

    unsubmitted_drafts = (
        ParsedDraft.objects.filter(user=request.user, kind='company')
        .exclude(state='submitted')
    )

    return render(
        request,
        'recruiters/dashboard.html',
        {
            'verification': verification,
            'total_jobs': total_jobs,
            'active_jobs': active_jobs,
            'total_applicants': total_applicants,
            'unsubmitted_drafts': unsubmitted_drafts,
            'is_verified': request.user.is_verified_recruiter,
        }
    )


@recruiter_required
def submit_verification(request):
    """Step 1: Upload NTN and SECP documents."""
    form = CompanyDocsForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        for label, key in (('ntn', 'ntn_cert'), ('secp', 'secp_cert')):
            f = form.cleaned_data.get(key)
            if f:
                d = ParsedDraft.objects.create(
                    user=request.user,
                    kind='company',
                    label=label,
                    file=f
                )
                enqueue(d.id)
        messages.info(request, 'Documents uploaded. Extracting details with AI for your review...')
        return redirect('review_company')
    return render(request, 'recruiters/submit.html', {'form': form})


@recruiter_required
def review_company(request):
    """Step 2: Review autofilled company details and submit for admin approval."""
    drafts = (
        ParsedDraft.objects.filter(user=request.user, kind='company')
        .exclude(state='submitted')
    )

    if drafts.filter(state='pending').exists():
        return render(request, 'recruiters/processing.html')

    merged = merged_company_data(drafts)
    instance = RecruiterVerification.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = VerificationForm(request.POST, instance=instance)
        if form.is_valid():
            v = form.save(commit=False)
            v.user = request.user
            v.ntn_on_atl = check_atl(v.ntn)
            v.flags = company_flags(form.cleaned_data, merged)

            # Assign certificate files from drafts
            for d in drafts:
                if d.label == 'ntn':
                    v.ntn_cert = d.file.name
                elif d.label == 'secp':
                    v.incorporation_cert = d.file.name

            v.status = 'pending'
            v.reviewer_note = ''
            v.save()
            drafts.update(state='submitted')
            messages.success(request, 'Verification request submitted! Our staff will review your credentials.')
            return redirect('verification_status')
    else:
        form = VerificationForm(instance=instance, initial=None if instance else merged)

    return render(
        request,
        'recruiters/review_company.html',
        {
            'form': form,
            'drafts': drafts,
            'merged': merged,
        }
    )


@recruiter_required
def verification_status(request):
    v = RecruiterVerification.objects.filter(user=request.user).first()
    return render(request, 'recruiters/status.html', {'v': v})
