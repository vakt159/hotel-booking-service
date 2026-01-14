import stripe
from django.conf import settings

from payment.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(payment: Payment, success_url: str, cancel_url: str):
    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": f"Booking #{payment.booking.id}"},
                "unit_amount": int(payment.money_to_pay * 100),
            },
            "quantity": 1,
        }],
        success_url=success_url,
        cancel_url=cancel_url,
    )

    payment.session_id = session.id
    payment.session_url = session.url
    payment.save()

    return session.url
