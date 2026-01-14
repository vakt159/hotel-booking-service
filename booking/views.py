from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet

from booking.filters import BookingFilter
from booking.models import Booking
from booking.serializers import BookingReadSerializer


class BookingViewSet(ReadOnlyModelViewSet):
    queryset = Booking.objects.select_related("room", "user")
    serializer_class = BookingReadSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookingFilter

