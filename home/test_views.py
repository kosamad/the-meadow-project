"""
 Home application view tests
"""

from django.test import TestCase

class TestHomeViews(TestCase):

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        
