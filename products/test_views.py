from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Product 


class TestProductViews(TestCase):

    def setUp(self):
        image_path = 'media/full-logo.png'
        with open(image_path, 'rb') as img:
            image_data = img.read()

        self.product = Product.objects.create(
            name='Test Product',
            friendly_name='Test Product',
            price=19.99,
            description='This is a test product description.',
            has_sizes=True,
            alt_text='Test Product Image',
            rating=4.5,
            is_gift_card=False,
            is_active=True,
            size='M',
            image=SimpleUploadedFile('test_image.jpg', image_data, content_type='image/jpeg')
        )

    def test_get_products_page(self):
        url = reverse('product_detail', args=[self.product.id])
        response = self.client.get(url)       
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')