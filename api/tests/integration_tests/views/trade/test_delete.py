import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Trade

pytestmark = pytest.mark.integration


class TradeDeleteIntegrationTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('trades-list')
        self.url_delete = reverse('trades-detail', args=[1])

    def test_delete_ok(self):
        request_data = {
            'type': 'buy',
            'user_id': 23,
            'symbol': 'ABX',
            'shares': 30,
            'price': 134,
            'timestamp': 1531522701000
        }
        self.client.post(self.url, data=request_data)

        response = self.client.delete(self.url_delete)

        assert Trade.objects.count() == 0
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_not_found(self):
        response = self.client.delete(self.url_delete)
        response_data = response.json()

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response_data['detail'] == 'Not found.'
