from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from candidates.models import CandidateProfile, Education, WorkExperience
from parsing.models import ParsedDraft

User = get_user_model()


class CandidateReviewTests(TestCase):
    def setUp(self):
        self.candidate1 = User.objects.create_user(
            username='c1@example.com',
            email='c1@example.com',
            password='password123',
            is_candidate=True
        )
        self.profile1 = CandidateProfile.objects.create(user=self.candidate1, full_name='Candidate One')

        self.candidate2 = User.objects.create_user(
            username='c2@example.com',
            email='c2@example.com',
            password='password123',
            is_candidate=True
        )
        self.profile2 = CandidateProfile.objects.create(user=self.candidate2, full_name='Candidate Two')

        # Draft belonging to candidate 1
        cv_file = SimpleUploadedFile('c1_cv.pdf', b'%PDF-1.4 dummy')
        self.draft1 = ParsedDraft.objects.create(
            user=self.candidate1,
            kind='cv',
            label='cv',
            file=cv_file,
            state='ready',
            data={
                'full_name': 'Ali Hassan',
                'phone': '+923001234567',
                'city': 'Lahore',
                'headline': 'Full Stack Developer',
                'skills': ['Python', 'Django', 'React'],
                'experience_years': 4,
                'education': [{'degree': 'BS Computer Science', 'institute': 'FAST NUCES', 'year': '2018-2022'}],
                'experience': [{'title': 'Backend Developer', 'company': 'TechSys', 'start': '2022', 'end': 'Present', 'description': 'API engineering'}]
            }
        )

    def test_review_cv_get_shows_prefilled_values(self):
        """Test 5a: CV review GET shows prefilled values."""
        self.client.force_login(self.candidate1)
        url = reverse('review_cv', args=[self.draft1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'candidates/review_cv.html')
        # Check prefilled form initial values
        form = response.context['form']
        self.assertEqual(form.initial['full_name'], 'Ali Hassan')
        self.assertEqual(form.initial['city'], 'Lahore')
        self.assertEqual(form.initial['skills'], 'Python, Django, React')
        self.assertEqual(form.initial['experience_years'], 4)

    def test_review_cv_post_creates_profile_and_submits_draft(self):
        """Test 5b: CV review POST creates profile data, education and experience rows, and marks draft submitted."""
        self.client.force_login(self.candidate1)
        url = reverse('review_cv', args=[self.draft1.id])

        post_data = {
            'full_name': 'Ali Hassan Updated',
            'phone': '+923009999999',
            'city': 'Islamabad',
            'headline': 'Senior Software Architect',
            'skills': 'Python, Django, PostgreSQL, Kubernetes',
            'experience_years': 5,
            # Education formset
            'edu-TOTAL_FORMS': '1',
            'edu-INITIAL_FORMS': '0',
            'edu-MIN_NUM_FORMS': '0',
            'edu-MAX_NUM_FORMS': '1000',
            'edu-0-degree': 'MS Software Engineering',
            'edu-0-institute': 'NUST',
            'edu-0-year': '2022-2024',
            # Experience formset
            'exp-TOTAL_FORMS': '1',
            'exp-INITIAL_FORMS': '0',
            'exp-MIN_NUM_FORMS': '0',
            'exp-MAX_NUM_FORMS': '1000',
            'exp-0-title': 'Tech Lead',
            'exp-0-company': 'GlobalTech',
            'exp-0-start': '2024',
            'exp-0-end': 'Present',
            'exp-0-description': 'Leading backend infrastructure',
        }

        response = self.client.post(url, post_data)
        self.assertRedirects(response, reverse('candidate_dashboard'))

        self.profile1.refresh_from_db()
        self.assertEqual(self.profile1.full_name, 'Ali Hassan Updated')
        self.assertEqual(self.profile1.city, 'Islamabad')
        self.assertEqual(self.profile1.experience_years, 5)

        # Check education & experience created
        self.assertEqual(Education.objects.filter(profile=self.profile1).count(), 1)
        edu = Education.objects.filter(profile=self.profile1).first()
        self.assertEqual(edu.degree, 'MS Software Engineering')
        self.assertEqual(edu.institute, 'NUST')

        self.assertEqual(WorkExperience.objects.filter(profile=self.profile1).count(), 1)
        exp = WorkExperience.objects.filter(profile=self.profile1).first()
        self.assertEqual(exp.title, 'Tech Lead')

        # Check draft state updated to submitted
        self.draft1.refresh_from_db()
        self.assertEqual(self.draft1.state, 'submitted')

    def test_another_user_cannot_open_someones_draft(self):
        """Test 6: Another user cannot open someone else's draft (404)."""
        self.client.force_login(self.candidate2)
        url = reverse('review_cv', args=[self.draft1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
