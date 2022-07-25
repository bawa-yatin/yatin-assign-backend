from django.urls import path, include
from payments.views import stripe_webhook

urlpatterns = [
    path('api/stripe/', include('payments.urls')),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
]
