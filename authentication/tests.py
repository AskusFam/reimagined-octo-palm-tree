from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from .views import RegisterView
from django.contrib.auth.models import User
import json
# Create your tests here.


class AuthRegisterTest(APITestCase):
    @classmethod
    def setUp(cls):
        cls.client = APIClient()
        cls.url = reverse('auth_register')
        User.objects.create_user(
            username='TestingUser', email='testuser@gmail.com', password='testing123')
        cls.user = User.objects.get(username='TestingUser')

    def test_post_register_user_bad_password(self):
        response = self.client.post(self.url, {
            "username": "whoo",
            "email": "whoot@gmail.com",
            "password": "testing!",
            "password2": "testing"
        })
        self.assertEqual(response.status_code, 400)
    def test_post_register_user_isStaff_password2(self):
        response = self.client.post(self.url, {
            "username": "whoo",
            "email": "whoot@gmail.com",
            "password": "testing!",
            "is_staff": "True"
        })
        self.assertEqual(response.status_code, 400)

    def test_post_register_user_good(self):
        response = self.client.post(self.url, {
            "username": "whoo",
            "email": "whoot@gmail.com",
            "password": "testing!",
            "password2": "testing!"
        })
        self.assertEqual(response.status_code, 201)

    