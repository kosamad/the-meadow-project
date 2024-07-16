from django.apps import AppConfig

# Import Signals module and override ready method
class CheckoutConfig(AppConfig):
    name = 'checkout'

    def ready(self):
        import checkout.signals
