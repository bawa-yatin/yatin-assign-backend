from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import ProductDetails
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeCheckoutView(APIView):
    def post(self, request):
        data = request.data
        global quantity
        quantity = data['quantity']
        global product_name
        product_name = data['product']

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': 'price_1LOFkRSGJZ7JUrEoLBidJ9GK',
                        'quantity': quantity,
                    },
                ],
                payment_method_types=['card', ],
                mode='payment',
                success_url=settings.SITE_DOMAIN + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_DOMAIN + '/?canceled=true',
            )

            return redirect(checkout_session.url)
        except:
            return Response({"error": "Something went wrong while creating payment checkout session"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                            )


@csrf_exempt
def stripe_webhook(request):
    payload = request.body

    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        create_order(session)

    return HttpResponse(status=200)


def create_order(session):
    customer_name = session["customer_details"]["name"]
    customer_email = session["customer_details"]["email"]
    order_total = session["amount_total"]
    payment_method = session["payment_method_types"][0]

    str_amt = str(order_total)
    paid_amount = str_amt[:-2]

    ProductDetails.objects.create(user_name=customer_name, user_email=customer_email, product_name=product_name,
                                  product_quantity=quantity, total_amount=paid_amount, payment_method=payment_method)
