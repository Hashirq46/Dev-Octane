from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from candidates.models import CandidateProfile
from jobs.models import Application, Job
from recruiters.models import RecruiterVerification

User = get_user_model()


class JobsAndApplicationsTests(TestCase):
    def setUp(self):
        # Recruiter 1 (Approved)
        self.recruiter1 = User.objects.create_user(
            username='hr@alpha.pk',
            email='hr@alpha.pk',
            password='password123',
            is_recruiter=True
        )
        self.cert = SimpleUploadedFile('cert.pdf', b'%PDF-1.4 cert')
        self.v1 = RecruiterVerification.objects.create(
            user=self.recruiter1,
            company_name='Alpha Tech',
            ntn='1234567-1',
            status='approved',
            ntn_cert=self.cert
        )

        # Recruiter 2 (Unapproved / Pending)
        self.recruiter2 = User.objects.create_user(
            username='hr@beta.pk',
            email='hr@beta.pk',
            password='password123',
            is_recruiter=True
        )
        self.v2 = RecruiterVerification.objects.create(
            user=self.recruiter2,
            company_name='Beta Corp',
            ntn='7654321-2',
            status='pending',
            ntn_cert=self.cert
        )

        # Unrelated Recruiter 3
        self.recruiter3 = User.objects.create_user(
            username='hr@gamma.pk',
            email='hr@gamma.pk',
            password='password123',
            is_recruiter=True
        )

        # Candidate 1 (with CV)
        self.candidate1 = User.objects.create_user(
            username='applicant1@example.com',
            email='applicant1@example.com',
            password='password123',
            is_candidate=True
        )
        self.resume_file = SimpleUploadedFile('resume1.pdf', b'%PDF-1.4 resume')
        self.profile1 = CandidateProfile.objects.create(
            user=self.candidate1,
            full_name='Applicant One',
            resume=self.resume_file
        )

        # Candidate 2 (Unrelated Candidate)
        self.candidate2 = User.objects.create_user(
            username='applicant2@example.com',
            email='applicant2@example.com',
            password='password123',
            is_candidate=True
        )
        self.profile2 = CandidateProfile.objects.create(
            user=self.candidate2,
            full_name='Applicant Two',
            resume=self.resume_file
        )

        # Staff User
        self.staff_user = User.objects.create_superuser(
            username='admin@example.com',
            email='admin@example.com',
            password='password123'
        )

        # Job posted by Recruiter 1
        self.job1 = Job.objects.create(
            recruiter=self.recruiter1,
            title='Django Backend Engineer',
            description='Build awesome platforms',
            city='Lahore',
            is_active=True
        )

        # Job posted by Recruiter 2
        self.job2 = Job.objects.create(
            recruiter=self.recruiter2,
            title='Frontend Engineer',
            description='React and UI',
            city='Karachi',
            is_active=True
        )

    def test_candidate_cannot_apply_twice_to_same_job(self):
        """Test 10a: Candidate cannot apply twice to the same job."""
        self.client.force_login(self.candidate1)
        apply_url = reverse('apply', args=[self.job1.id])

        # 1st apply
        res1 = self.client.post(apply_url)
        self.assertRedirects(res1, reverse('job_detail', args=[self.job1.id]))
        self.assertEqual(Application.objects.filter(job=self.job1, candidate=self.candidate1).count(), 1)

        # 2nd apply attempt
        res2 = self.client.post(apply_url)
        self.assertRedirects(res2, reverse('job_detail', args=[self.job1.id]))
        self.assertEqual(Application.objects.filter(job=self.job1, candidate=self.candidate1).count(), 1)

    def test_recruiter_cannot_see_another_recruiters_applications(self):
        """Test 10b: Recruiter cannot see another recruiter's applications."""
        # Candidate 1 applies to Job 1 (Recruiter 1)
        Application.objects.create(job=self.job1, candidate=self.candidate1)

        # Recruiter 3 tries to view applicants for Job 1
        self.client.force_login(self.recruiter3)
        res = self.client.get(reverse('job_applicants', args=[self.job1.id]))
        self.assertEqual(res.status_code, 404)

        # Recruiter 1 CAN view applicants for Job 1
        self.client.force_login(self.recruiter1)
        res_owner = self.client.get(reverse('job_applicants', args=[self.job1.id]))
        self.assertEqual(res_owner.status_code, 200)
        self.assertContains(res_owner, 'Applicant One')

    def test_resume_download_permissions(self):
        """Test 11: Resume download allowed for owner, staff, and recruiter with an application; 404 for others."""
        download_url = reverse('download_resume', args=[self.profile1.id])

        # 1. Anonymous user -> redirected to login
        self.client.logout()
        res_anon = self.client.get(download_url)
        self.assertRedirects(res_anon, f"{reverse('login')}?next={download_url}")

        # 2. Unrelated candidate (Candidate 2) -> 404
        self.client.force_login(self.candidate2)
        res_other_cand = self.client.get(download_url)
        self.assertEqual(res_other_cand.status_code, 404)

        # 3. Recruiter without an application -> 404
        self.client.force_login(self.recruiter1)
        res_recruiter_no_app = self.client.get(download_url)
        self.assertEqual(res_recruiter_no_app.status_code, 404)

        # Candidate 1 applies to Job 1
        Application.objects.create(job=self.job1, candidate=self.candidate1)

        # 4. Recruiter 1 (now has application) -> Allowed (200)
        self.client.force_login(self.recruiter1)
        res_recruiter_with_app = self.client.get(download_url)
        self.assertEqual(res_recruiter_with_app.status_code, 200)
        self.assertEqual(res_recruiter_with_app['Content-Type'], 'application/pdf')

        # 5. Candidate 1 (owner) -> Allowed (200)
        self.client.force_login(self.candidate1)
        res_owner = self.client.get(download_url)
        self.assertEqual(res_owner.status_code, 200)

        # 6. Staff User -> Allowed (200)
        self.client.force_login(self.staff_user)
        res_staff = self.client.get(download_url)
        self.assertEqual(res_staff.status_code, 200)

    def test_verified_badge_appears_only_for_approved_recruiters(self):
        """Test 12: Verified badge appears only for approved recruiters."""
        # Check Job 1 detail page (Recruiter 1 is approved)
        res1 = self.client.get(reverse('job_detail', args=[self.job1.id]))
        self.assertEqual(res1.status_code, 200)
        self.assertContains(res1, '✔ Verified')

        # Check Job 2 detail page (Recruiter 2 is pending)
        res2 = self.client.get(reverse('job_detail', args=[self.job2.id]))
        self.assertEqual(res2.status_code, 200)
        self.assertNotContains(res2, '✔ Verified')
