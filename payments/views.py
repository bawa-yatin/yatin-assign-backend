import os
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import ProductDetails

# Stripe secret key for authenticating API requests
stripe.api_key = settings.STRIPE_SECRET_KEY
price_id = os.environ.get('PRICE_ID')


# Class view for rendering built-in stripe checkout page on the basis of quantity
# selected.
class StripeCheckoutView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        global quantity
        quantity = data['quantity']
        global product_name
        product_name = data['product']

        try:
            # Creation of checkout session consisting of line items,currency, and
            # acceptable payment methods which customer will see on checkout page.
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': price_id,
                        'quantity': quantity,
                    },
                ],
                payment_method_types=['card', ],
                mode='payment',  # Specified 'payment' mode for one-time payments

                # Success and Cancel URLs for redirecting the customer after successful
                # purchase or on cancellation of order.
                success_url=settings.SITE_DOMAIN + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_DOMAIN + '/?canceled=true',
            )

            # After creation of session, redirecting customer to the URL for the
            # checkout page returned in response.
            return redirect(checkout_session.url)
        except:
            return Response({"error": "Something went wrong while creating payment checkout session"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                            )


# Event handler so stripe can send checkout session completed event when a customer
# completes checkout
@csrf_exempt
def stripe_webhook(request):
    payload = request.body  # payload contains the event that is returned after
    # successful payment

    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    # Verifying webhook that came from stripe using the payload, Stripe signature,
    # and Stripe webhook secret. If the webhook is verified we can then access
    # the data from the event
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        create_order(session)

    return HttpResponse(status=200)


# Function for fetching order details from the passed argument and saving it inside
# the database
def create_order(session):
    customer_name = session["customer_details"]["name"]
    customer_email = session["customer_details"]["email"]
    order_total = session["amount_total"]
    payment_method = session["payment_method_types"][0]

    str_amt = str(order_total)
    paid_amount = str_amt[:-2]

    ProductDetails.objects.create(user_name=customer_name, user_email=customer_email, product_name=product_name,
                                  product_quantity=quantity, total_amount=paid_amount, payment_method=payment_method)
