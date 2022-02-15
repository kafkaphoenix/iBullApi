import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Trade

pytestmark = pytest.mark.integration


class TradeCreateIntegrationTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('trades-list')

    def test_create_ok(self):
        request_data = {
            'type': 'buy',
            'user_id': 23,
            'symbol': 'ABX',
            'shares': 30,
            'price': 134,
            'timestamp': 1531522701000
        }

        response = self.client.post(self.url, data=request_data)
        response_data = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert Trade.objects.count() == 1
        assert Trade.objects.filter(timestamp=1531522701000).values().first() == response_data

    def test_required_fields_ko(self):
        request_data = {}

        response = self.client.post(self.url, data=request_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Trade.objects.count(), 0)

    def test_wrong_type_ko(self):
        request_data = {
            'type': 'buya',
            'user_id': 23,
            'symbol': 'ABX',
            'shares': 30,
            'price': 134,
            'timestamp': 1531522701000
        }

        response = self.client.post(self.url, data=request_data)
        response_data = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data['type'] == ['Enter a valid value.']

    def test_wrong_type_and_exceeded_size_ko(self):
        request_data = {
            'type': 'sella',
            'user_id': 23,
            'symbol': 'ABX',
            'shares': 30,
            'price': 134,
            'timestamp': 1531522701000
        }

        response = self.client.post(self.url, data=request_data)
        response_data = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data['type'] == ['Enter a valid value.', 'Ensure this field has no more than 4 characters.']

    def test_min_user_id_ko(self):
        request_data = {
            'type': 'buy',
            'user_id': 0,
            'symbol': 'ABX',
            'shares': 2,
            'price': 134,
            'timestamp': 1531522701000
        }

        response = self.client.post(self.url, data=request_data)
        response_data = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data['user_id'] == ['Ensure this value is greater than or equal to 1.']

    def test_symbol_exceeded_size_ko(self):
        request_data = {
            'type': 'buy',
            'user_id': 23,
            'symbol': 'ABXppppppppppppppppp',
            'shares': 2,
            'price': 134,
            'timestamp': 1531522701000
        }

        response = self.client.post(self.url, data=request_data)
        response_data = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data['symbol'] == ['Ensure this field has no more than 10 characters.']

    def test_max_shares_ko(self):
        request_data = {
            'type': 'buy',
            'user_id': 23,
            'symbol': 'ABX',
            'shares': 1220,
            'price': 134,
            'timestamp': 1531522701000
        }

        response = self.client.post(self.url, data=request_data)
        response_data = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data['shares'] == ['Ensure this value is less than or equal to 100.']

    def test_min_shares_ko(self):
        request_data = {
            'type': 'buy',
            'user_id': 23,
            'symbol': 'ABX',
            'shares': -2,
            'price': 134,
            'timestamp': 1531522701000
        }

        response = self.client.post(self.url, data=request_data)
        response_data = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data['shares'] == ['Ensure this value is greater than or equal to 1.']

    def test_min_price_ko(self):
        request_data = {
            'type': 'buy',
            'user_id': 1,
            'symbol': 'ABX',
            'shares': 2,
            'price': -23,
            'timestamp': 1531522701000
        }

        response = self.client.post(self.url, data=request_data)
        response_data = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data['price'] == ['Ensure this value is greater than or equal to 0.']

    def test_min_timestamp_ko(self):
        request_data = {
            'type': 'buy',
            'user_id': 1,
            'symbol': 'ABX',
            'shares': 2,
            'price': 23,
            'timestamp': -2
        }

        response = self.client.post(self.url, data=request_data)
        response_data = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data['timestamp'] == ['Ensure this value is greater than or equal to 0.']
