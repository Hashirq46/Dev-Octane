from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('post/', views.post_job, name='post_job'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('<int:job_id>/close/', views.close_job, name='close_job'),
    path('<int:job_id>/apply/', views.apply, name='apply'),
    path('<int:job_id>/applicants/', views.job_applicants, name='job_applicants'),
    path('application/<int:app_id>/status/', views.update_application_status, name='update_application_status'),
]
