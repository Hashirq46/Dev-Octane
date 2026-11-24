from functools import wraps
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def candidate_required(view):
    @wraps(view)
    def wrapper(request, *a, **kw):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_candidate:
            return HttpResponseForbidden('Candidates only.')
        return view(request, *a, **kw)
    return wrapper


def recruiter_required(view):
    @wraps(view)
    def wrapper(request, *a, **kw):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_recruiter:
            return HttpResponseForbidden('Recruiters only.')
        return view(request, *a, **kw)
    return wrapper


def verified_recruiter_required(view):
    @recruiter_required
    @wraps(view)
    def wrapper(request, *a, **kw):
        v = getattr(request.user, 'recruiterverification', None)
        if v is None:
            messages.info(request, 'Verify your company to post jobs.')
            return redirect('submit_verification')
        if v.status != 'approved':
            messages.info(request, 'Your verification is under review or needs changes.')
            return redirect('verification_status')
        return view(request, *a, **kw)
    return wrapper
