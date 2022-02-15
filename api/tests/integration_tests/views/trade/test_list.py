import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Trade

pytestmark = pytest.mark.integration


class TradeListIntegrationTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('trades-list')

    def test_list_ok(self):
        request_data = {
            'type': 'buy',
            'user_id': 23,
            'symbol': 'ABX',
            'shares': 30,
            'price': 134,
            'timestamp': 1531522701000
        }
        self.client.post(self.url, data=request_data)
        request_data2 = {
            'type': 'buy',
            'user_id': 2,
            'symbol': 'GME',
            'shares': 20,
            'price': 14,
            'timestamp': 1531522731000
        }
        self.client.post(self.url, data=request_data2)

        response = self.client.get(self.url)
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(response_data) == Trade.objects.count()
        first_trade = Trade.objects.filter(timestamp__in=[1531522701000]).values().first()
        second_trade = Trade.objects.filter(timestamp__in=[1531522731000]).values().first()
        assert response_data == [first_trade, second_trade]
