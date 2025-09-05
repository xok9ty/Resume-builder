from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.
class ProfileViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('profile')

    def test_profilke_return_correct(self):
        response = self.client.get(self.url)
        self.assertAlmostEqual(response.status_code, 200)