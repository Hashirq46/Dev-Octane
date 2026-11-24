import tempfile
import os
import pandas as pd
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from recruiters.models import ActiveTaxpayer, RecruiterVerification
from recruiters.services import company_flags

User = get_user_model()


class RecruiterVerificationTests(TestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(
            username='hr@systems.com',
            email='hr@systems.com',
            password='password123',
            is_recruiter=True
        )
        self.cert_file = SimpleUploadedFile('ntn.pdf', b'%PDF-1.4 dummy')

    def test_unverified_recruiter_cannot_reach_post_job_approved_can(self):
        """Test 7: Unverified recruiter cannot reach post_job; approved recruiter can."""
        self.client.force_login(self.recruiter)
        post_job_url = reverse('post_job')

        # 1. No verification record -> redirected to submit_verification
        res_none = self.client.get(post_job_url)
        self.assertRedirects(res_none, reverse('submit_verification'))

        # 2. Verification pending -> redirected to verification_status
        v = RecruiterVerification.objects.create(
            user=self.recruiter,
            company_name='Systems Limited',
            ntn='1234567-8',
            status='pending',
            ntn_cert=self.cert_file
        )
        res_pending = self.client.get(post_job_url)
        self.assertRedirects(res_pending, reverse('verification_status'))

        # 3. Approved recruiter -> reaches post_job successfully (200)
        v.status = 'approved'
        v.save()
        res_approved = self.client.get(post_job_url)
        self.assertEqual(res_approved.status_code, 200)
        self.assertTemplateUsed(res_approved, 'jobs/post.html')

    def test_editing_ntn_after_approval_resets_status_to_pending(self):
        """Test 8: Editing NTN after approval resets status to pending."""
        v = RecruiterVerification.objects.create(
            user=self.recruiter,
            company_name='Systems Limited',
            ntn='1234567-8',
            status='approved',
            ntn_cert=self.cert_file
        )
        self.assertEqual(v.status, 'approved')
        self.assertTrue(self.recruiter.is_verified_recruiter)

        # Recruiter modifies NTN
        v.ntn = '7654321-0'
        v.save()
        v.refresh_from_db()

        self.assertEqual(v.status, 'pending')
        self.assertFalse(self.recruiter.is_verified_recruiter)

    def test_company_flags_logic(self):
        """Test 9: company_flags flags NTN mismatch, name mismatch, and missing ATL entry."""
        # Setup ActiveTaxpayer table
        ActiveTaxpayer.objects.create(ntn='1234567', name='Verified Tech PK')

        typed = {
            'company_name': 'My Super Tech Solutions',
            'ntn': '9999999-9',  # Not on ATL
            'cuin': '',           # No CUIN
        }
        extracted = {
            'company_name': 'Completely Different Name Ltd',
            'ntn': '1234567-8',
        }

        flags = company_flags(typed, extracted)

        # Verify all flags are generated
        self.assertTrue(any('NTN entered differs' in f for f in flags))
        self.assertTrue(any('Company name differs' in f for f in flags))
        self.assertTrue(any('NTN not found in imported Active Taxpayer List' in f for f in flags))
        self.assertTrue(any('No CUIN provided' in f for f in flags))

    def test_import_atl_command(self):
        """Test import_atl management command with a CSV file."""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False, mode='w', encoding='utf-8') as f:
            f.write("Sr,Registration_NTN,Taxpayer_Name\n")
            f.write("1,1122334-4,Alpha Tech Pvt Ltd\n")
            f.write("2,5566778-8,Beta Global Solutions\n")
            temp_path = f.name

        try:
            call_command('import_atl', temp_path)
            self.assertTrue(ActiveTaxpayer.objects.filter(ntn='11223344').exists())
            self.assertTrue(ActiveTaxpayer.objects.filter(ntn='55667788').exists())
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
