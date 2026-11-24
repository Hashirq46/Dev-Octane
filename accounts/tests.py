from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()


class AuthTests(TestCase):
    def test_recruiter_signup_free_email_rejected(self):
        """Test 1a: Recruiter signup with @gmail.com is rejected."""
        url = reverse('recruiter_signup')
        response = self.client.post(url, {
            'email': 'recruiter@gmail.com',
            'password': 'ComplexPassword123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'email', 'Please use your official company email address.')
        self.assertFalse(User.objects.filter(email='recruiter@gmail.com').exists())

    def test_recruiter_signup_official_email_succeeds(self):
        """Test 1b: Recruiter signup with company domain succeeds and user is inactive until confirmed."""
        url = reverse('recruiter_signup')
        response = self.client.post(url, {
            'email': 'recruiter@techcorp.pk',
            'password': 'ComplexPassword123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/check_email.html')

        user = User.objects.filter(email='recruiter@techcorp.pk').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.is_recruiter)
        self.assertFalse(user.is_candidate)
        self.assertFalse(user.is_active)  # Inactive until email confirmation

    def test_email_confirmation_valid_and_invalid_tokens(self):
        """Test 2: Valid and invalid confirmation tokens."""
        user = User.objects.create_user(
            username='user@company.pk',
            email='user@company.pk',
            password='ComplexPassword123!',
            is_active=False
        )
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        # Test invalid token
        invalid_url = reverse('confirm_email', kwargs={'uidb64': uidb64, 'token': 'invalid-token-123'})
        res_invalid = self.client.get(invalid_url)
        self.assertEqual(res_invalid.status_code, 200)
        self.assertTemplateUsed(res_invalid, 'accounts/invalid_link.html')
        user.refresh_from_db()
        self.assertFalse(user.is_active)

        # Test valid token
        valid_url = reverse('confirm_email', kwargs={'uidb64': uidb64, 'token': token})
        res_valid = self.client.get(valid_url)
        self.assertRedirects(res_valid, reverse('login'))
        user.refresh_from_db()
        self.assertTrue(user.is_active)
