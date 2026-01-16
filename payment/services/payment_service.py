from payment.exceptions import PendingPaymentExists
from payment.models import Payment


def create_booking_payment(booking):
    if booking.payments.filter(
        status=Payment.PaymentStatus.PENDING
    ).exists():
        raise PendingPaymentExists()

    nights = (booking.check_out_date - booking.check_in_date).days
    amount = booking.price_per_night * nights

    payment = Payment.objects.create(
        booking=booking,
        type=Payment.PaymentType.BOOKING,
        status=Payment.PaymentStatus.PENDING,
        money_to_pay=amount,
    )
    return payment
