import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(payment,success_url, cancel_url):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": f"Booking #{payment.booking.id} | Room {payment.booking.room.number}",
                },
                "unit_amount": int(payment.money_to_pay * 100),
            },
            "quantity": 1,
        }],
    )

    payment.session_id = session.id
    payment.session_url = session.url
    payment.save(update_fields=["session_id", "session_url"])

    return payment
