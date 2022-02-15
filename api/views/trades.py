from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter, BooleanFilter
from rest_framework.viewsets import ModelViewSet

from api.models import Trade
from api.serializers.trade import TradeSerializer


class TradeViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'delete',)
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'user_id']
