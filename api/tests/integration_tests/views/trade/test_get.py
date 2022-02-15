import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Trade

pytestmark = pytest.mark.integration


class TradeGetIntegrationTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('trades-list')
        self.url_get = reverse('trades-detail', args=[1])

    def test_get_ok(self):
        request_data = {
            'type': 'buy',
            'user_id': 23,
            'symbol': 'ABX',
            'shares': 30,
            'price': 134,
            'timestamp': 1531522701000
        }
        self.client.post(self.url, data=request_data)

        response = self.client.get(self.url_get)
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert Trade.objects.filter(timestamp=1531522701000).values().first() == response_data

    def test_not_found(self):
        response = self.client.get(self.url_get)
        response_data = response.json()

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response_data['detail'] == 'Not found.'
