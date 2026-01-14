from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from booking.filters import BookingFilter
from booking.models import Booking
from booking.serializers import (
    BookingReadSerializer,
    BookingCreateSerializer
)


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingReadSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookingFilter

    def get_queryset(self):
        queryset = Booking.objects.select_related("room", "user")

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return BookingCreateSerializer
        return BookingReadSerializer

    def create(self, request, *args, **kwargs):
        """Create new booking with user auto-attachment and price from room."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        response_serializer = BookingReadSerializer(booking)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )
