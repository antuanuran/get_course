from rest_framework.permissions import IsAuthenticated

from apps.api.serializers.purchases import PurchaseSerializer
from apps.api.views.base import BaseModelViewSet
from apps.purchases.models import Purchase


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
