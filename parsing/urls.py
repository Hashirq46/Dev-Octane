from django.urls import path
from . import views

urlpatterns = [
    path('draft-status/<int:draft_id>/', views.draft_status, name='draft_status'),
]
