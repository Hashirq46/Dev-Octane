from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from jobs import views as job_views
from parsing import views as parsing_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', job_views.home, name='home'),
    path('privacy/', TemplateView.as_view(template_name='privacy.html'), name='privacy'),

    # App URLs
    path('', include('accounts.urls')),
    path('candidate/', include('candidates.urls')),
    path('recruiter/', include('recruiters.urls')),
    path('jobs/', include('jobs.urls')),
    path('parsing/', include('parsing.urls')),

    # Protected file downloads
    path('download/resume/<int:profile_id>/', parsing_views.download_resume, name='download_resume'),
    path('download/certificate/<int:verification_id>/<str:cert_type>/', parsing_views.download_certificate, name='download_certificate'),
]
