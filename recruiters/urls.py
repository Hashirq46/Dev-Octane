from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('submit-verification/', views.submit_verification, name='submit_verification'),
    path('review-company/', views.review_company, name='review_company'),
    path('verification-status/', views.verification_status, name='verification_status'),
]
