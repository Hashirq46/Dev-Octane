from django.urls import path
from . import views

urlpatterns = [
    path('review-cv/<int:draft_id>/', views.review_cv, name='review_cv'),
    path('dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]
