from rest_framework.test import APIClient, APITestCase
from .serializers import PhotoSerializer 
from unittest.mock import patch
from .models import Photo
from django.urls import reverse

from .views import PhotosListCreate, PhotoRetrieveUpdateDestroy
from django.contrib.auth.models import User
from PIL import Image
import tempfile
# Create your tests here.


class PhotosListCreateTest(APITestCase):
    @classmethod
    def setUp(cls):
        cls.client = APIClient()
        cls.url = reverse('photos_home')
        User.objects.create_user(
            username='TestingUser', email='testuser@gmail.com', password='testing123')
        cls.user = User.objects.get(username='TestingUser')

        cls.view = PhotosListCreate.as_view()


    def test_get_photos_unauth_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_get_photos_auth_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

    def test_get_photos_auth_user2(self):
        Photo.objects.create(title='testPhoto', year='2023', created_at='2023-04-10T22:37:03.965293Z', updated_at='2023-04-10T22:37:03.965293Z',
                             path_to_store='images/557772ae-7c32-43ad-b3d6-fd610ba6bc1e', creator=self.user)
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)

    @patch('photos.views.create_photo')
    def test_post_photos_success(self, mock_create_photo):
        im = Image.open('img/pexels-belle-co-1000445.jpg')
        self.client.force_authenticate(user=self.user)

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        im.save(tmp_file)
        tmp_file.seek(0)
        mock_create_photo.return_value = '/testing/mock/path'
        response = self.client.post(self.url, {
                "title": "Testing New Image Tests Mode",
                "year": "2023",
                "image": tmp_file
            })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(mock_create_photo.called)

    def test_post_photos_fail(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url, {
                "title": "Testing New Image Tests Mode",
                "year": "2023"
            })
        self.assertEqual(response.status_code, 400)

    