from django.contrib import admin
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.html import format_html
from .models import ActiveTaxpayer, RecruiterVerification


def _notify(v, subject, body):
    send_mail(subject, body, None, [v.user.email])


@admin.action(description='Approve selected')
def approve(modeladmin, request, qs):
    for v in qs:
        v.status = 'approved'
        v.reviewed_by = request.user
        v.reviewed_at = timezone.now()
        v.save()
        _notify(
            v,
            'Your company is verified',
            'Your company has been verified. You can now post jobs and your Verified badge is active.'
        )


@admin.action(description='Reject selected (add a reviewer note first)')
def reject(modeladmin, request, qs):
    for v in qs:
        v.status = 'rejected'
        v.reviewed_by = request.user
        v.reviewed_at = timezone.now()
        v.save()
        _notify(
            v,
            'Company verification needs changes',
            f"Your verification was not approved.\n\nReason: {v.reviewer_note or 'Please check your details and resubmit.'}"
        )


@admin.register(RecruiterVerification)
class RecruiterVerificationAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'ntn', 'cuin', 'ntn_on_atl', 'status', 'created_at', 'view_certificates')
    list_filter = ('status', 'ntn_on_atl')
    search_fields = ('company_name', 'ntn', 'cuin', 'user__email')
    readonly_fields = ('flags', 'ntn_on_atl', 'created_at', 'reviewed_by', 'reviewed_at', 'admin_checklist_guide')
    actions = [approve, reject]

    fieldsets = (
        ('Verification Checklist & Instructions', {
            'fields': ('admin_checklist_guide',),
        }),
        ('Company Information', {
            'fields': ('user', 'company_name', 'ntn', 'cuin', 'address', 'city')
        }),
        ('Uploaded Certificates (Private)', {
            'fields': ('ntn_cert', 'incorporation_cert')
        }),
        ('Automated Sanity Signals', {
            'fields': ('ntn_on_atl', 'flags', 'created_at')
        }),
        ('Review & Decision', {
            'fields': ('status', 'reviewer_note', 'reviewed_by', 'reviewed_at')
        }),
    )

    def admin_checklist_guide(self, obj):
        return format_html(
            """
            <div style="background: #fff3cd; padding: 12px; border-left: 4px solid #ffc107; font-size: 13px;">
                <strong>Manual Admin Review Checklist:</strong><br>
                1. Open <a href="https://eservices.secp.gov.pk" target="_blank">eservices.secp.gov.pk</a>, search the CUIN, and confirm the company name matches.<br>
                2. Confirm the company name and NTN match the uploaded certificates.<br>
                3. Confirm the recruiter's email domain matches the company website or name.<br>
                4. Carefully review all automatic flags below.
            </div>
            """
        )
    admin_checklist_guide.short_description = "Checklist Guidance"

    def view_certificates(self, obj):
        links = []
        if obj.ntn_cert:
            links.append(f'<a href="/download/certificate/{obj.id}/ntn/">NTN Cert</a>')
        if obj.incorporation_cert:
            links.append(f'<a href="/download/certificate/{obj.id}/secp/">SECP Cert</a>')
        return format_html(' | '.join(links) or 'None')
    view_certificates.short_description = "Certificates"


@admin.register(ActiveTaxpayer)
class ActiveTaxpayerAdmin(admin.ModelAdmin):
    list_display = ('ntn', 'name', 'imported_at')
    search_fields = ('ntn', 'name')
    ordering = ('-imported_at',)
