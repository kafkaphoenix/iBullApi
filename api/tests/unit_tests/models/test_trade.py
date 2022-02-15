import decimal

import pytest
from django.test import TestCase

from api.models import Trade

pytestmark = pytest.mark.unit


class TradeUnitTestCase(TestCase):
    def test_str(self):
        trade = Trade(type='buy', user_id=23, symbol='AEX', shares=22, price=decimal.Decimal(12), timestamp=2333332)

        assert str(trade) == f'{trade.user_id}: {trade.symbol}-{trade.shares}'
