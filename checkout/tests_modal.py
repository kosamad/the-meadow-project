from django.test import TestCase
from decimal import Decimal
from products.models import Product, ProductVariant, Event
from profiles.models import UserProfile
from django.contrib.auth.models import User
from .models import Order, ProductOrderLineItem, EventOrderLineItem
from datetime import timedelta
from django.utils import timezone


class OrderModelTests(TestCase):

    def setUp(self):
        # Create or retrieve a User instance (prevent unique contraint errors)
        user, created = User.objects.get_or_create(username="testuser8")
        if created:
            user.set_password("password8")
            user.save()

        # Create or retrieve a UserProfile instance associated with the User
        self.user_profile, _ = UserProfile.objects.get_or_create(user=user)
       
        # Prodcut Instance
        self.product = Product.objects.create(
            name="Test Product",
            price=Decimal('10.00')
        ) 

        # Create an Order instance
        self.order = Order.objects.create(
            user_profile=self.user_profile,
            full_name="User Test",
            email="testuser8@example.com",
            phone_number="1234567890",
            postcode="12345",
            town_or_city="Test Town",
            street_address1="123 Test Street",
            street_address2="Bristol",
            county="Test County",
            delivery_cost=Decimal('5.00'),
            order_total=Decimal('100.00'),
            grand_total=Decimal('105.00'),
            original_bag="[]",
            stripe_pid="test_stripe_pid"
        )


    def test_order_creation(self):
            """
            Test the creation of an Order instance and its attributes.
            """
            self.assertIsInstance(self.order, Order)
            self.assertEqual(self.order.full_name, "User Test")
            self.assertEqual(self.order.email, "testuser8@example.com")
            self.assertEqual(self.order.phone_number, "1234567890")
            self.assertEqual(self.order.postcode, "12345")
            self.assertEqual(self.order.town_or_city, "Test Town")
            self.assertEqual(self.order.street_address1, "123 Test Street")
            self.assertEqual(self.order.street_address2, "Bristol")
            self.assertEqual(self.order.county, "Test County")
            self.assertEqual(self.order.delivery_cost, Decimal('5.00'))
            self.assertEqual(self.order.order_total, Decimal('100.00'))
            self.assertEqual(self.order.grand_total, Decimal('105.00'))
            self.assertEqual(self.order.original_bag, "[]")
            self.assertEqual(self.order.stripe_pid, "test_stripe_pid")


    def test_order_with_events(self):
        """
        Test that the order total calculation is correct when events are included.
        """
        event_datetime = timezone.now() + timedelta(days=1)
        
        event = Event.objects.create(name="Test Event", 
        price=Decimal('55.00'), 
        event_datetime=event_datetime )

        EventOrderLineItem.objects.create(
            order=self.order,
            event=event,
            quantity=1,
            lineitem_total=event.price,
        )

        self.order.update_total()

        # Check totals
        self.assertEqual(self.order.order_total, event.price)
        self.assertEqual(self.order.grand_total, self.order.order_total + self.order.delivery_cost)


    def test_product_order_lineitem_total(self):
        """
        Test that the ProductOrderLineItem's lineitem_total is calculated.
        """

        line_item = ProductOrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=3,
        )
        expected_total = self.product.price * 3
        self.assertEqual(line_item.lineitem_total, expected_total)


    def test_event_order_lineitem_total(self):
        """
        Test that the EventOrderLineItem's lineitem_total is calculated 
        """
        event_datetime = timezone.now() + timedelta(days=1)
        event = Event.objects.create(name="Test Event", price=Decimal('55.00'), event_datetime=event_datetime)
        line_item = EventOrderLineItem.objects.create(
            order=self.order,
            event=event,
            quantity=2,
        )
        expected_total = event.price * 2
        self.assertEqual(line_item.lineitem_total, expected_total)