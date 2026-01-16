from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from booking.models import Booking
from booking.services import mark_no_show_bookings
from room.models import Room
from django.contrib.auth import get_user_model


class MarkNoShowBookingsTests(TestCase):
    def setUp(self):
        self.room = Room.objects.create(
            number="101",
            capacity=2,
            price_per_night="100.00",
        )
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            password="testpass123",
        )

    def test_mark_no_show_bookings_updates_only_past_check_in_bookings(self):
        today = timezone.localdate()

        past_booking = Booking.objects.create(
            room=self.room,
            user=self.user,
            check_in_date=today - timedelta(days=2),
            check_out_date=today + timedelta(days=2),
            status=Booking.BookingStatus.BOOKED,
            price_per_night="100.00",
        )

        future_booking = Booking.objects.create(
            room=self.room,
            user=self.user,
            check_in_date=today + timedelta(days=2),
            check_out_date=today + timedelta(days=5),
            status=Booking.BookingStatus.BOOKED,
            price_per_night="100.00",
        )

        updated_count = mark_no_show_bookings()

        self.assertEqual(updated_count, 1)

        past_booking.refresh_from_db()
        future_booking.refresh_from_db()

        self.assertEqual(past_booking.status, Booking.BookingStatus.NO_SHOW)
        self.assertEqual(future_booking.status, Booking.BookingStatus.BOOKED)

    def test_mark_no_show_bookings_does_not_touch_non_booked_statuses(self):
        today = timezone.localdate()

        active_booking = Booking.objects.create(
            room=self.room,
            user=self.user,
            check_in_date=today - timedelta(days=5),
            check_out_date=today + timedelta(days=2),
            status=Booking.BookingStatus.ACTIVE,
            price_per_night="100.00",
        )

        updated_count = mark_no_show_bookings()

        self.assertEqual(updated_count, 0)

        active_booking.refresh_from_db()
        self.assertEqual(active_booking.status, Booking.BookingStatus.ACTIVE)

    def test_mark_no_show_bookings_returns_0_if_nothing_to_update(self):
        updated_count = mark_no_show_bookings()
        self.assertEqual(updated_count, 0)
