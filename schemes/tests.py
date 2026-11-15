from django.test import TestCase
from django.contrib.auth.models import User
from .models import Scheme, SchemeApplication


class SchemeListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='organizer', password='testpass123', is_staff=True)
        self.scheme = Scheme.objects.create(
            name='Test Scholarship',
            description='A test scholarship for students.',
            category='education',
            organization='Ministry of Education',
            min_age=18,
            max_age=25,
            max_income=500000,
            status='active',
            created_by=self.user,
        )

    def test_home_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_scheme_list_loads(self):
        response = self.client.get('/schemes/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Scholarship')

    def test_scheme_detail_loads(self):
        response = self.client.get(f'/schemes/{self.scheme.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Scholarship')

    def test_scheme_detail_slug_loads(self):
        response = self.client.get(f'/schemes/detail/{self.scheme.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_scheme_api_returns_json(self):
        response = self.client.get('/schemes/api/list/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_scheme_by_category(self):
        response = self.client.get('/schemes/category/education/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Scholarship')

    def test_scheme_search(self):
        response = self.client.get('/schemes/?q=Scholarship')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Scholarship')

    def test_404_for_nonexistent_scheme(self):
        response = self.client.get('/schemes/9999/')
        self.assertEqual(response.status_code, 404)


class SchemeApplicationTest(TestCase):
    def setUp(self):
        self.organizer = User.objects.create_user(username='organizer', password='testpass123', is_staff=True)
        self.user = User.objects.create_user(username='citizen', password='testpass123')
        self.scheme = Scheme.objects.create(
            name='Housing Scheme',
            description='Affordable housing for all.',
            category='housing',
            organization='Ministry of Housing',
            status='active',
            created_by=self.organizer,
        )

    def test_apply_requires_login(self):
        response = self.client.get(f'/schemes/{self.scheme.pk}/apply/')
        self.assertEqual(response.status_code, 302)

    def test_apply_to_scheme(self):
        self.client.login(username='citizen', password='testpass123')
        response = self.client.post(f'/schemes/{self.scheme.pk}/apply/', {
            'reason': 'I need affordable housing.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SchemeApplication.objects.filter(user=self.user, scheme=self.scheme).exists())
