import os
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404
from candidates.models import CandidateProfile
from jobs.models import Application
from recruiters.models import RecruiterVerification
from .models import ParsedDraft


@login_required
def draft_status(request, draft_id):
    d = get_object_or_404(ParsedDraft, pk=draft_id, user=request.user)
    return JsonResponse({'state': d.state})


@login_required
def download_resume(request, profile_id):
    p = get_object_or_404(CandidateProfile, pk=profile_id)
    allowed = (
        request.user == p.user
        or request.user.is_staff
        or (
            request.user.is_recruiter
            and Application.objects.filter(candidate=p.user, job__recruiter=request.user).exists()
        )
    )
    if not allowed or not p.resume:
        raise Http404
    return FileResponse(
        p.resume.open('rb'),
        as_attachment=True,
        filename=os.path.basename(p.resume.name)
    )


@login_required
def download_certificate(request, verification_id, cert_type):
    v = get_object_or_404(RecruiterVerification, pk=verification_id)
    allowed = request.user == v.user or request.user.is_staff
    if not allowed:
        raise Http404

    if cert_type == 'ntn':
        file_obj = v.ntn_cert
    elif cert_type == 'secp':
        file_obj = v.incorporation_cert
    else:
        raise Http404

    if not file_obj:
        raise Http404

    return FileResponse(
        file_obj.open('rb'),
        as_attachment=True,
        filename=os.path.basename(file_obj.name)
    )
