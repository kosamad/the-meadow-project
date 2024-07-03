
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Product, Category, Event
from datetime import datetime, timedelta
from django.utils import timezone


"""
Products model tests
"""


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



"""
Events model tests
"""
class TestEventModel(TestCase):

    def setUp(self):
        self.event_datetime = timezone.now() + timedelta(days=5)
        self.event = Event.objects.create(
            name='Base Event',
            friendly_name='Friendly Base Event',
            price=29.99,
            event_datetime=self.event_datetime,
            description='Description for Base Event',
            capacity=100,
            tickets_sold=50,
            image=None,
            alt_text='Alt text for Base Event',
            is_active=True
        )
    # Test event creation 
    def test_event_creation(self):
        self.assertIsInstance(self.event, Event)
        self.assertEqual(str(self.event), 'Base Event')
        self.assertEqual(self.event.friendly_name, 'Friendly Base Event')
        self.assertEqual(self.event.price, 29.99)      
        self.assertEqual(self.event.description, 'Description for Base Event')
        self.assertEqual(self.event.capacity, 100)
        self.assertEqual(self.event.tickets_sold, 50)
        self.assertEqual(self.event.event_datetime, self.event_datetime)     
   
    # Testing Event Order
    def test_event_ordering(self):
        self.event1 = Event.objects.create(
            name='Event 1',
            price=29.99,
            capacity=100,
            tickets_sold=50,
            event_datetime=timezone.now() - timedelta(days=1)
        )
        self.event2 = Event.objects.create(
            name='Event 2',
            price=29.99,
            capacity=100,
            tickets_sold=50,
            event_datetime=timezone.now()
        )
        self.event3 = Event.objects.create(
            name='Event 3',
            price=29.99,
            capacity=100,
            tickets_sold=50,
            event_datetime=timezone.now() + timedelta(days=1)
        )
        ordered_events = Event.objects.order_by('event_datetime')
        self.assertEqual(list(ordered_events), [self.event1, self.event2, self.event3, self.event])

    # Testing image upload works.
    def test_image_field(self):
        image_path = 'media/full-logo.png'
        with open(image_path, 'rb') as img:
            image_data = img.read()

        event_with_image = Event.objects.create(
            name='Event 1',
            friendly_name='Friendly Event 1',
            price=29.99,
            event_datetime=self.event_datetime,
            description='Description for Event 1',
            capacity=100,
            tickets_sold=50,
            image=SimpleUploadedFile('test_image.jpg', image_data, content_type='image/jpeg'),
            alt_text='Alt text for Event 1',
            is_active=True
        )

        saved_event = Event.objects.get(id=event_with_image.id)
        self.assertIsNotNone(saved_event.image)

    






