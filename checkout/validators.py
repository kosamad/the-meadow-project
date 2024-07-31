from django.core.exceptions import ValidationError
from django.utils import timezone

# Prevents product order delivery date from being in the past

def validate_date(date):
    if date < timezone.now().date():
        raise ValidationError("Date cannot be in the past")