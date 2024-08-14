from django.test import TestCase
from products.models import Product, Event
from blog.models import Post
from django.urls import reverse
from datetime import datetime


class PostModelTest(TestCase):
    # Post with an associated product
    def setUp(self):
        self.product = Product.objects.create(friendly_name="Test Product")        
        self.post = Post.objects.create(
            title="Test Post",
            image="test_image.jpg",
            alt_text="Test Alt Text",
            product=self.product,            
            body="This is a test post body."
        )
        
    
    # Blog post created with correct data
    def test_post_creation(self):
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.alt_text, "Test Alt Text")
        self.assertEqual(self.post.body, "This is a test post body.")
        self.assertEqual(self.post.product, self.product)        
        self.assertTrue(isinstance(self.post.date, datetime))


    # String method correct
    def test_post_str_method(self):
        self.assertEqual(str(self.post), "Test Post")