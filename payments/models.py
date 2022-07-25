from datetime import datetime
from django.db import models


class ProductDetails(models.Model):
    user_name = models.CharField(max_length=100, blank=False, null=False)
    user_email = models.EmailField(max_length=100, unique=True,blank=False, null=False)
    product_name = models.CharField(max_length=100, blank=False, null=False)
    product_quantity = models.IntegerField()
    total_amount = models.IntegerField()
    payment_method = models.CharField(max_length=100, blank=False, null=False)
    order_created = models.DateTimeField(default=datetime.now, blank=True)
