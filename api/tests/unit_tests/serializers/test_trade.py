import decimal
import pdb

import pytest
from django.test import TestCase

from api.models import Trade
from api.serializers.trade import TradeSerializer

pytestmark = pytest.mark.unit


class TradeSerializerUnitTestCase(TestCase):
    def test_serializer_ok(self):
        trade = Trade(
            type='buy',
            user_id=23,
            symbol='ABX',
            shares=30,
            price=decimal.Decimal(134),
            timestamp=1531522701000
        )
        trade.save()
        json_data = {
            'id': 1,
            'type': 'buy',
            'user_id': 23,
            'symbol': 'ABX',
            'shares': 30,
            'price': 134,
            'timestamp': 1531522701000
        }

        serialized_data = TradeSerializer(trade)

        assert serialized_data.data == json_data
