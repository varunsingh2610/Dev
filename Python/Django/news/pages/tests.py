from django.test import SimpleTestCase, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class HomePageTests(SimpleTestCase):

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self