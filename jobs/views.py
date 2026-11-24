from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from accounts.decorators import candidate_required, recruiter_required, verified_recruiter_required
from .forms import JobForm
from .models import Application, Job


def home(request):
    latest_jobs = (
        Job.objects.filter(is_active=True)
        .select_related('recruiter', 'recruiter__recruiterverification')
        .order_by('-created_at')[:8]
    )
    total_jobs = Job.objects.filter(is_active=True).count()
    cities = Job.objects.filter(is_active=True).values_list('city', flat=True).distinct()[:6]

    return render(
        request,
        'jobs/home.html',
        {
            'latest_jobs': latest_jobs,
            'total_jobs': total_jobs,
            'cities': cities,
        }
    )


def job_list(request):
    qs = Job.objects.filter(is_active=True).select_related('recruiter', 'recruiter__recruiterverification')
    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(skills__icontains=q))
    if request.GET.get('city'):
        qs = qs.filter(city__iexact=request.GET['city'].strip())
    if request.GET.get('job_type'):
        qs = qs.filter(job_type=request.GET['job_type'].strip())
    if request.GET.get('category'):
        qs = qs.filter(category__iexact=request.GET['category'].strip())
    if request.GET.get('min_salary'):
        try:
            min_sal = int(request.GET['min_salary'])
            qs = qs.filter(salary_max__gte=min_sal)
        except ValueError:
            pass

    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'jobs/list.html',
        {
            'page': page,
            'q': q,
            'selected_city': request.GET.get('city', ''),
            'selected_job_type': request.GET.get('job_type', ''),
            'selected_category': request.GET.get('category', ''),
            'selected_min_salary': request.GET.get('min_salary', ''),
            'job_types': Job.JobType.choices,
        }
    )


def job_detail(request, job_id):
    job = get_object_or_404(
        Job.objects.select_related('recruiter', 'recruiter__recruiterverification'),
        pk=job_id
    )
    has_applied = False
    if request.user.is_authenticated and request.user.is_candidate:
        has_applied = Application.objects.filter(job=job, candidate=request.user).exists()

    return render(
        request,
        'jobs/detail.html',
        {
            'job': job,
            'has_applied': has_applied,
        }
    )


@candidate_required
def apply(request, job_id):
    job = get_object_or_404(Job, pk=job_id, is_active=True)
    profile = getattr(request.user, 'candidate_profile', None)
    if not profile or not profile.resume:
        messages.warning(request, 'Please upload your CV before applying.')
        return redirect('edit_profile')

    app, created = Application.objects.get_or_create(job=job, candidate=request.user)
    if created:
        messages.success(request, 'Application submitted.')
    else:
        messages.info(request, 'You have already applied for this job.')
    return redirect('job_detail', job_id=job.id)


@verified_recruiter_required
def post_job(request):
    form = JobForm(request.POST or None)
    if form.is_valid():
        job = form.save(commit=False)
        job.recruiter = request.user
        job.save()
        messages.success(request, 'Job opening created successfully!')
        return redirect('job_detail', job_id=job.pk)
    return render(request, 'jobs/post.html', {'form': form})


@verified_recruiter_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id, recruiter=request.user)
    form = JobForm(request.POST or None, instance=job)
    if form.is_valid():
        form.save()
        messages.success(request, 'Job opening updated successfully.')
        return redirect('job_detail', job_id=job.pk)
    return render(request, 'jobs/edit.html', {'form': form, 'job': job})


@verified_recruiter_required
def close_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id, recruiter=request.user)
    job.is_active = False
    job.save()
    messages.success(request, f'Job "{job.title}" has been closed.')
    return redirect('my_jobs')


@recruiter_required
def my_jobs(request):
    jobs = (
        Job.objects.filter(recruiter=request.user)
        .annotate(applicant_count=Count('applications'))
        .order_by('-created_at')
    )
    return render(request, 'jobs/my_jobs.html', {'jobs': jobs})


@recruiter_required
def job_applicants(request, job_id):
    job = get_object_or_404(Job, pk=job_id, recruiter=request.user)
    applications = (
        Application.objects.filter(job=job)
        .select_related('candidate', 'candidate__candidate_profile')
        .order_by('-applied_at')
    )
    return render(
        request,
        'jobs/applicants.html',
        {
            'job': job,
            'applications': applications,
            'status_choices': Application.Status.choices,
        }
    )


@recruiter_required
def update_application_status(request, app_id):
    app = get_object_or_404(Application, pk=app_id, job__recruiter=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Application.Status.choices):
            app.status = new_status
            app.save()
            messages.success(request, f'Application status updated to {app.get_status_display()}.')
    return redirect('job_applicants', job_id=app.job.id)
