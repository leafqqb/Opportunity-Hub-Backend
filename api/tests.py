from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationTests(APITestCase):
    def test_register_and_login_user(self):
        url = reverse('auth-register')
        payload = {
            'username': 'student1',
            'email': 'student1@example.com',
            'password': 'Pass12345!',
            'role': 'student',
            'headline': 'University student',
            'bio': 'Interested in internships.',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['username'], 'student1')

        login_url = reverse('auth-login')
        login_response = self.client.post(login_url, {'username': 'student1', 'password': 'Pass12345!'}, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('token', login_response.data)


class OpportunityTests(APITestCase):
    def setUp(self):
        register_url = reverse('auth-register')
        payload = {
            'username': 'company1',
            'email': 'company1@example.com',
            'password': 'Pass12345!',
            'role': 'company',
            'company_name': 'Acme Co',
        }
        response = self.client.post(register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_create_update_delete_opportunity(self):
        create_url = reverse('opportunity-list')
        payload = {
            'title': 'Summer Internship',
            'organization_name': 'Acme Co',
            'description': 'A short internship for students.',
            'opportunity_type': 'Internship',
            'category': 'Engineering',
            'location': 'Remote',
            'external_url': 'https://example.com/apply',
        }
        response = self.client.post(create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        opp_id = response.data['id']

        detail_url = reverse('opportunity-detail', args=[opp_id])
        patch_response = self.client.patch(detail_url, {'location': 'Hybrid'}, format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.data['location'], 'Hybrid')

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.client.get(detail_url).status_code, status.HTTP_404_NOT_FOUND)
