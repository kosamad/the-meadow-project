"""
Products application model tests
"""

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Product, Category


class TestProductModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category", friendly_name="Test Category")

    def test_product_created_correctly(self):
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            friendly_name="Test Product",
            price=19.99,
            description="This is a test product",
            has_sizes=True,
            alt_text="Test Product Image",
            rating=4.5,
            is_gift_card=False,
            is_active=True,
            size='M'
        )
        
        # Product instance is of type Product
        self.assertIsInstance(self.product, Product)
        
        # Other attributes of the product
        self.assertEqual(self.product.__str__(), self.product.name)
        self.assertEqual(self.product.price, 19.99)
        self.assertEqual(self.product.description, "This is a test product")
        self.assertEqual(self.product.has_sizes, True)
        self.assertEqual(self.product.alt_text, "Test Product Image")
        self.assertEqual(self.product.rating, 4.5)
        self.assertEqual(self.product.is_gift_card, False)
        self.assertEqual(self.product.is_active, True)
        self.assertEqual(self.product.size, 'M')

    # testing default ordering of products.
    def test_product_ordering(self):
        self.category = Category.objects.create(name="Test Category", friendly_name="Test Category")
        # Products created (req fields only), when passes also confirms image, rating and  size can be left blank or null as intended.
        self.product1 = Product.objects.create(
            category=self.category,
            name="Product 1",
            friendly_name="B Product",
            price=19.99,
            description="This is product 1",
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name="Product 2",
            friendly_name="A Product",
            price=29.99,
            description="This is product 2",
        )
        self.product3 = Product.objects.create(
            category=self.category,
            name="Product 3",
            friendly_name="C Product",
            price=39.99,
            description="This is product 3",
        )
        # Retrieve all products and check the ordering
        ordered_products = Product.objects.all()    
        self.assertEqual(list(ordered_products), [self.product2, self.product1, self.product3])
        
    # Testing image upload works.
    def test_image_field(self):
        image_path = 'media/full-logo.png'
        with open(image_path, 'rb') as img:
            image_data = img.read()

        product = Product.objects.create(
            category=self.category,
            name="Test Image Product",
            friendly_name="Test Image Product",
            price=19.99,
            description="This is a test product with an image",
            has_sizes=True,
            alt_text="Test Product Image",
            image=SimpleUploadedFile('test_image.jpg', image_data, content_type='image/jpeg')
        )

        saved_product = Product.objects.get(id=product.id)
        self.assertIsNotNone(saved_product.image)


