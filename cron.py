from django.utils import timezone
from datetime import timedelta

from main.models import Order

def delete_expired_orders(self, *args, **options):
    # Delete orders that have expired and are still unfulfilled
    threshold_time = timezone.now()
    Order.objects.filter(expiry_time__lte=threshold_time, fulfilled=False).delete()