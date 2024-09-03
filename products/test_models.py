
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Product, Category, Event, ProductVariant
from datetime import datetime, timedelta
from django.utils import timezone
import uuid


"""
Category model tests
"""


class CategoryModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            friendly_name='Test Friendly Category'
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Test Category')

    def test_get_friendly_name(self):
        self.assertEqual(self.category.get_friendly_name(), 'Test Friendly Category')


"""
Products model tests
"""


class TestProductModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category", friendly_name="Test Category")
        image_path = 'media/full-logo.png'
        with open(image_path, 'rb') as img_file:
            self.image_data = img_file.read()

    def test_product_created_correctly(self):
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            friendly_name='Test Friendly Product',
            price=8.00,
            description='Test product description',
            image=SimpleUploadedFile('test_image.jpg', self.image_data, content_type='image/jpeg'),
            alt_text='Test Product Image',
            is_gift_card=False,
            is_active=True,
            is_infinite_stock=False
        )

        # Product instance is of type Product
        self.assertIsInstance(self.product, Product)

        # Other attributes of the product
        self.assertEqual(self.product.__str__(), self.product.name)
        self.assertEqual(self.product.price, 8.00)
        self.assertEqual(self.product.description, "Test product description")
        self.assertIsNotNone(self.product.image)
        self.assertEqual(self.product.alt_text, "Test Product Image")
        self.assertEqual(self.product.is_gift_card, False)
        self.assertEqual(self.product.is_active, True)

    # testing default ordering of products.
    def test_product_ordering(self):
        self.category = Category.objects.create(name="Test Category", friendly_name="Test Category")
        # Products created (req fields only), when passes also confirms image, rating and  size can be left blank or null as intended.
        self.product1 = Product.objects.create(
            category=self.category,
            name="Product 1",
            friendly_name="B Product",
            price=8.00,
            description="This is product 1",
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name="Product 2",
            friendly_name="A Product",
            price=9.00,
            description="This is product 2",
        )
        self.product3 = Product.objects.create(
            category=self.category,
            name="Product 3",
            friendly_name="C Product",
            price=5.00,
            description="This is product 3",
        )
        # Retrieve all products and check the ordering
        ordered_products = Product.objects.all()
        self.assertEqual(list(ordered_products), [self.product2, self.product1, self.product3])


"""
Product Variant model tests
"""


class TestProductVariantModel(TestCase):

    def setUp(self):
        # Create a category for the product
        self.category = Category.objects.create(name="Test Category", friendly_name="Test Category")

        # Create a product to associate with the product variants
        self.product = Product.objects.create(
            name='Test Product',
            friendly_name='Friendly Test Product',
            price=19.99,
            description='Description for Test Product',
            image=SimpleUploadedFile('test_product_image.jpg', b'test image data', content_type='image/jpeg'),
            alt_text='Test Product Image',
            is_gift_card=False,
            is_active=True,
            is_infinite_stock=False
        )

    def test_product_variant_creation(self):
        # Create a product variant
        variant = ProductVariant.objects.create(
            product=self.product,
            size='M',
            is_infinite_stock=False,
            price=5.00,
            is_active=True
        )

        # Test that the variant is created and has the correct attributes
        self.assertIsInstance(variant, ProductVariant)
        self.assertEqual(variant.product, self.product)
        self.assertEqual(variant.size, 'M')
        self.assertFalse(variant.is_infinite_stock)
        self.assertEqual(variant.price, 5.00)
        self.assertTrue(variant.is_active)

    def test_product_variant_unique_constraint(self):
        # Create a product variant with the same size for the same product
        ProductVariant.objects.create(
            product=self.product,
            size='S',
            is_infinite_stock=False,
            price=6.00,
            is_active=True
        )

        # Try to create a duplicate variant with the same size for the same product
        with self.assertRaises(Exception) as context:
            ProductVariant.objects.create(
                product=self.product,
                size='S',
                stock=3,
                is_infinite_stock=True,
                price=10.00,
                is_active=True
            )

        self.assertTrue('UNIQUE constraint failed' in str(context.exception))


"""
Events model tests
"""


class TestEventModel(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Event Category", friendly_name="Event Category")
        self.event_datetime = timezone.now() + timedelta(days=5)
        self.image_data = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'This is a test image content',
            content_type='image/jpeg'
        )

        self.event = Event.objects.create(
            name='test Event',
            friendly_name='Friendly Test Event',
            price=8.00,
            event_datetime=self.event_datetime,
            description='Description for Test Event',
            duration_hours=3,
            image=self.image_data,
            alt_text='Alt text for test Event',
            is_active=True
        )

    # Testing Event Creation
    def test_event_creation(self):
        # Retrieve the event from the database
        saved_event = Event.objects.get(id=self.event.id)

        # Assertions
        self.assertIsInstance(saved_event, Event)
        self.assertEqual(str(saved_event), 'test Event')
        self.assertEqual(saved_event.friendly_name, 'Friendly Test Event')
        self.assertEqual(saved_event.price, 8.00)
        self.assertEqual(saved_event.description, 'Description for Test Event')
        self.assertEqual(saved_event.event_datetime, self.event_datetime)
        self.assertEqual(saved_event.duration_hours, 3)
        self.assertIsNotNone(saved_event.image)  # Ensure image is uploaded
        self.assertTrue(saved_event.image.name.startswith('event_images/test_image'))  # Check if the image is stored with a prefix
        self.assertEqual(saved_event.alt_text, 'Alt text for test Event')
        self.assertTrue(saved_event.is_active)
        self.assertTrue(saved_event.is_event)
