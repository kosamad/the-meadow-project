from django.test import TestCase
from django.urls import reverse

"""
 About application view tests
"""

class TestAboutView(TestCase):

    def test_about_page(self):
        # Use the reverse function to get the URL for the about page
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/about.html')