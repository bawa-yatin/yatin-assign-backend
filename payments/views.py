from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeCheckoutView(APIView):
    def post(self, request):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': 'price_1LOFkRSGJZ7JUrEoLBidJ9GK',
                        'quantity': 1,
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
