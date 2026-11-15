from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Profile


class RegisterViewTest(TestCase):
    def test_register_page_loads(self):
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')

    def test_register_creates_user_and_profile(self):
        response = self.client.post('/accounts/register/', {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'securepass123',
            'confirm_password': 'securepass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(Profile.objects.filter(user__username='testuser').exists())


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_login_page_loads(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_login_successful(self):
        response = self.client.post('/accounts/login/', {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)


class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        Profile.objects.create(user=self.user)
        self.client.login(username='testuser', password='testpass123')

    def test_profile_requires_login(self):
        self.client.logout()
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 302)

    def test_profile_page_loads(self):
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)
