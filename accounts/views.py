from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django_ratelimit.decorators import ratelimit

from candidates.models import CandidateProfile
from parsing.models import ParsedDraft
from parsing.tasks import enqueue
from .forms import CandidateSignupForm, RecruiterSignupForm, ResendConfirmationForm

User = get_user_model()


def send_confirmation(request, user):
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    link = request.build_absolute_uri(
        reverse('confirm_email', kwargs={'uidb64': uidb64, 'token': token})
    )
    subject = 'Confirm your JobPortal account'
    body = (
        f"Hello,\n\n"
        f"Please click the link below to confirm your email and activate your JobPortal account:\n\n"
        f"{link}\n\n"
        f"If you did not create an account, please disregard this email."
    )
    send_mail(subject, body, None, [user.email])


@ratelimit(key='ip', rate='5/h', method='POST', block=True)
def candidate_signup(request):
    form = CandidateSignupForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        with transaction.atomic():
            user = form.save()
            CandidateProfile.objects.create(user=user, full_name=form.cleaned_data['full_name'])
            draft = ParsedDraft.objects.create(
                user=user,
                kind='cv',
                label='cv',
                file=form.cleaned_data['cv']
            )
        send_confirmation(request, user)
        enqueue(draft.id)
        return render(request, 'accounts/check_email.html', {'email': user.email})
    return render(request, 'accounts/candidate_signup.html', {'form': form})


@ratelimit(key='ip', rate='5/h', method='POST', block=True)
def recruiter_signup(request):
    form = RecruiterSignupForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        send_confirmation(request, user)
        return render(request, 'accounts/check_email.html', {'email': user.email})
    return render(request, 'accounts/recruiter_signup.html', {'form': form})


def confirm_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been confirmed! Please sign in.')
        return redirect('login')
    return render(request, 'accounts/invalid_link.html')


@ratelimit(key='ip', rate='5/h', method='POST', block=True)
def resend_confirmation(request):
    form = ResendConfirmationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email'].lower()
        user = User.objects.filter(email__iexact=email).first()
        if user and not user.is_active:
            send_confirmation(request, user)
        return render(request, 'accounts/check_email.html', {'email': email, 'resent': True})
    return render(request, 'accounts/resend_confirmation.html', {'form': form})


class RoleLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        u = self.request.user
        if u.is_recruiter:
            return reverse('recruiter_dashboard')
        if u.is_candidate:
            d = (
                ParsedDraft.objects.filter(user=u, kind='cv')
                .exclude(state='submitted')
                .order_by('-created_at')
                .first()
            )
            if d:
                return reverse('review_cv', args=[d.id])
            return reverse('candidate_dashboard')
        return reverse('home')
