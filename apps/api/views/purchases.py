from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.api.serializers.purchases import PurchaseSerializer
from apps.api.views.base import BaseModelViewSet
from apps.purchases.models import Purchase
from apps.purchases.service import LeadpayError, generate_leadpay_payment_link


class PurchaseViewSet(BaseModelViewSet):
    http_method_names = ["get", "head", "options", "post"]
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, queryset=None):
        qs = super().get_queryset(queryset).filter(user=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=["get"], detail=True, url_path="payment-link")
    def payment_link(self, request, *args, **kwargs):
        obj = self.get_object()

        try:
            link = generate_leadpay_payment_link(obj)
        except LeadpayError as ex:
            raise APIException(detail=str(ex), code=status.HTTP_424_FAILED_DEPENDENCY)

        return Response({"link": link}, status=status.HTTP_200_OK)


@api_view(http_method_names=["post"])
@permission_classes([AllowAny])
def notification_link(request, *args, **kwargs):
    # TODO: check ip addresses
    data = request.data
    obj = get_object_or_404(Purchase, id=data["order_id"])
    actual_status = {
        "success": obj.Status.COMPLETED,
        "fail": obj.Status.FAILED,
    }.get(data["status"], obj.Status.SUSPECTED)
    if obj.price != int(data["summa"]):
        actual_status = obj.Status.SUSPECTED
    obj.status = actual_status
    obj.save(update_fields=["status"])
    return Response(status=status.HTTP_200_OK)
