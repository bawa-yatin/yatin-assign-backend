from django.utils import timezone
from django.db import models


# Model class for storing order details in database after successful purchase
class ProductDetails(models.Model):
    user_name = models.CharField(max_length=100, blank=False, null=False)
    user_email = models.EmailField(max_length=100, blank=False, null=False)
    product_name = models.CharField(max_length=100, blank=False, null=False)
    product_quantity = models.IntegerField()
    total_amount = models.IntegerField()
    payment_method = models.CharField(max_length=100, blank=False, null=False)
    order_created = models.DateTimeField(default=timezone.now, blank=True)
