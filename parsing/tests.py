from datetime import timedelta
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from candidates.models import CandidateProfile
from parsing.models import ParsedDraft
from parsing.schemas import CVData
from parsing.tasks import parse_draft

User = get_user_model()


class ParsingTests(TestCase):
    def test_candidate_signup_creates_draft_and_rejects_bad_signature(self):
        """Test 3: Candidate signup creates user, profile, and pending draft; wrong signature is rejected."""
        url = reverse('candidate_signup')

        # 1. Invalid signature (claims to be PDF but content is not %PDF)
        bad_file = SimpleUploadedFile('my_resume.pdf', b'MALICIOUS_OR_CORRUPT_BYTES', content_type='application/pdf')
        res_bad = self.client.post(url, {
            'full_name': 'Ali Khan',
            'email': 'ali@gmail.com',  # candidates CAN use public emails
            'password': 'ComplexPassword123!',
            'cv': bad_file,
            'consent': 'on',
        })
        self.assertEqual(res_bad.status_code, 200)
        self.assertFormError(res_bad.context['form'], 'cv', 'File content does not match its extension.')
        self.assertFalse(User.objects.filter(email='ali@gmail.com').exists())

        # 2. Valid signature (%PDF)
        valid_pdf = SimpleUploadedFile('valid_cv.pdf', b'%PDF-1.4 valid test pdf content', content_type='application/pdf')
        with patch('parsing.tasks.parse_draft') as mock_task:
            res_good = self.client.post(url, {
                'full_name': 'Ali Khan',
                'email': 'ali@gmail.com',
                'password': 'ComplexPassword123!',
                'cv': valid_pdf,
                'consent': 'on',
            })
            self.assertEqual(res_good.status_code, 200)
            self.assertTemplateUsed(res_good, 'accounts/check_email.html')

            user = User.objects.filter(email='ali@gmail.com').first()
            self.assertIsNotNone(user)
            self.assertTrue(user.is_candidate)
            self.assertFalse(user.is_active)

            profile = CandidateProfile.objects.filter(user=user).first()
            self.assertIsNotNone(profile)
            self.assertEqual(profile.full_name, 'Ali Khan')

            draft = ParsedDraft.objects.filter(user=user, kind='cv').first()
            self.assertIsNotNone(draft)
            self.assertEqual(draft.state, 'pending')
            self.assertEqual(draft.label, 'cv')

    def test_parsing_task_mocked_extract_success_and_failure(self):
        """Test 4: Parsing task with mocked extract sets state=ready and fills data; when extract raises, state=failed."""
        user = User.objects.create_user(username='tester@example.com', email='tester@example.com', password='password123')
        test_file = SimpleUploadedFile('sample.pdf', b'%PDF-1.4 dummy content')
        draft = ParsedDraft.objects.create(user=user, kind='cv', label='cv', file=test_file)

        # Success case
        mock_data = CVData(
            full_name='Ali Ahmed',
            headline='Django Specialist',
            skills=['Python', 'Django'],
            experience_years=3
        )
        with patch('parsing.tasks.extract', return_value=mock_data):
            parse_draft(draft.id)
            draft.refresh_from_db()
            self.assertEqual(draft.state, 'ready')
            self.assertEqual(draft.data['full_name'], 'Ali Ahmed')
            self.assertEqual(draft.data['skills'], ['Python', 'Django'])

        # Failure case (e.g. Anthropic API network error or unparseable document)
        draft_fail = ParsedDraft.objects.create(user=user, kind='cv', label='cv', file=test_file)
        with patch('parsing.tasks.extract', side_effect=Exception('API Connection Timeout')):
            parse_draft(draft_fail.id)
            draft_fail.refresh_from_db()
            self.assertEqual(draft_fail.state, 'failed')
            self.assertEqual(draft_fail.data, {})

    def test_cleanup_drafts_command(self):
        """Test cleanup_drafts management command deletes unsubmitted drafts > 14 days old."""
        user = User.objects.create_user(username='clean@example.com', email='clean@example.com', password='password123')
        old_time = timezone.now() - timedelta(days=15)

        d_old_unsubmitted = ParsedDraft.objects.create(user=user, kind='cv', file=SimpleUploadedFile('old.pdf', b'%PDF-1.4'))
        ParsedDraft.objects.filter(id=d_old_unsubmitted.id).update(created_at=old_time)

        d_submitted = ParsedDraft.objects.create(user=user, kind='cv', state='submitted', file=SimpleUploadedFile('sub.pdf', b'%PDF-1.4'))
        ParsedDraft.objects.filter(id=d_submitted.id).update(created_at=old_time)

        d_recent = ParsedDraft.objects.create(user=user, kind='cv', state='pending', file=SimpleUploadedFile('rec.pdf', b'%PDF-1.4'))

        call_command('cleanup_drafts')

        self.assertFalse(ParsedDraft.objects.filter(id=d_old_unsubmitted.id).exists())
        self.assertTrue(ParsedDraft.objects.filter(id=d_submitted.id).exists())
        self.assertTrue(ParsedDraft.objects.filter(id=d_recent.id).exists())
