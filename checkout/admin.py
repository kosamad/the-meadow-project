from django.contrib import admin
from .models import Order, ProductOrderLineItem, EventOrderLineItem

# Add and edit line items in the admin panel
class ProductOrderLineItemAdminInline(admin.TabularInline):
    model = ProductOrderLineItem
    readonly_fields = ('lineitem_total',)


class EventOrderLineItemAdminInline(admin.TabularInline):
    model = EventOrderLineItem
    readonly_fields = ('lineitem_total',)
    

# Order admin configuration
class OrderAdmin(admin.ModelAdmin):
    inlines = (ProductOrderLineItemAdminInline, EventOrderLineItemAdminInline)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_bag', 'stripe_pid'
                        )

    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total','original_bag', 'stripe_pid')

    # Restrict display for order list
    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    # Order items by date
    ordering = ('-date',)



admin.site.register(Order, OrderAdmin)