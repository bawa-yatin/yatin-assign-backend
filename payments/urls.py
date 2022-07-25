from django.urls import path
from .views import StripeCheckoutView

# Url file for storing all urls made under 'payment' app.
urlpatterns = [
    path('create-checkout-session', StripeCheckoutView.as_view()),  # url path for
    # getting redirected to check out page
]
