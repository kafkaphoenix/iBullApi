# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework.test import RequestsClient
from json.decoder import JSONDecodeError

BASE_URL = 'http://localhost:8000'

user23_buy_ABX = {
    "type": "buy",
    "user_id": 23,
    "symbol": "ABX",
    "shares": 30,
    "price": 134,
    "timestamp": 1531522701000
}

user23_sell_AAC = {
    "type": "sell",
    "user_id": 23,
    "symbol": "AAC",
    "shares": 12,
    "price": 133,
    "timestamp": 1521522701000
}

user24_sell_AAC = {
    "type": "sell",
    "user_id": 24,
    "symbol": "AAC",
    "shares": 12,
    "price": 133,
    "timestamp": 1511522701000
}

user25_sell_AAC = {
    "type": "sell",
    "user_id": 25,
    "symbol": "AAC",
    "shares": 12,
    "price": 111,
    "timestamp": 1501522701000
}

all_users = [user23_buy_ABX, user23_sell_AAC, user24_sell_AAC, user25_sell_AAC]


def strip_id(user_dict):
    return {k: v for k, v in user_dict.items() if k != 'id'}


class TestCreate(TestCase):

    def setUp(self):
        self.client = RequestsClient()
        self.trade_types = ['sell', 'buy']
        self.min_shares = 1
        self.max_shares = 100

    def test_with_buy_type(self):
        user = user23_buy_ABX
        self.assertEqual(user['type'], 'buy')

        r = self.client.post(BASE_URL + '/trades/', json=user)
        self.assertEqual(r.status_code, 201)
        data = r.json()
        self.assertIn('id', data)
        self.assertIsInstance(data['id'], int)
        self.assertDictEqual(strip_id(data), user)

    def test_with_sell_type(self):
        user = user23_sell_AAC
        self.assertEqual(user['type'], 'sell')

        r = self.client.post(BASE_URL + '/trades/', json=user)
        self.assertEqual(r.status_code, 201)
        data = r.json()
        self.assertIn('id', data)
        self.assertIsInstance(data['id'], int)
        self.assertDictEqual(strip_id(data), user)

    def test_with_invalid_type(self):
        payload = user23_buy_ABX.copy()
        payload['type'] = 'foo'
        self.assertNotIn(payload['type'], self.trade_types)

        r = self.client.post(BASE_URL + '/trades/', json=payload)
        self.assertEqual(r.status_code, 400)

    def test_with_too_many_shares(self):
        payload = user23_buy_ABX.copy()
        payload['shares'] = self.max_shares + 1
        self.assertGreater(payload['shares'], self.max_shares)

        r = self.client.post(BASE_URL + '/trades/', json=payload)
        self.assertEqual(r.status_code, 400)

    def test_with_not_enough_shares(self):
        payload = user23_buy_ABX.copy()
        payload['shares'] = self.min_shares - 1
        self.assertLess(payload['shares'], self.min_shares)

        r = self.client.post(BASE_URL + '/trades/', json=payload)
        self.assertEqual(r.status_code, 400)


class TestGetTrades(TestCase):
    def setUp(self):
        self.client = RequestsClient()
        try:
            for user in all_users:
                self.client.post(BASE_URL + '/trades/', json=user)
        except JSONDecodeError:
            self.fail("/trades/ endpoint for POST request not implemented correctly")

    def test_without_filters(self):
        r = self.client.get(BASE_URL + '/trades/')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        without_ids = [strip_id(user) for user in data]
        self.assertListEqual(without_ids, all_users)

    def test_with_type_filter_buy(self):
        r = self.client.get(BASE_URL + '/trades/?type=buy')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        without_ids = [strip_id(user) for user in data]
        expected_trades = [user23_buy_ABX]
        self.assertListEqual(without_ids, expected_trades)

    def test_with_type_filter_sell(self):
        r = self.client.get(BASE_URL + '/trades/?type=sell')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        for user in data:
            self.assertIsInstance(user['id'], int)

        without_ids = [strip_id(user) for user in data]
        expected_trades = [user23_sell_AAC, user24_sell_AAC, user25_sell_AAC]
        self.assertListEqual(without_ids, expected_trades)

    def test_with_non_existing_type_filter(self):
        r = self.client.get(BASE_URL + '/trades/?type=boo')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertListEqual(data, [])

    def test_with_user_filter(self):
        r = self.client.get(BASE_URL + '/trades/?user_id=23')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        for user in data:
            self.assertIsInstance(user['id'], int)

        without_ids = [strip_id(user) for user in data]
        expected_trades = [user23_buy_ABX, user23_sell_AAC]
        self.assertListEqual(without_ids, expected_trades)

    def test_with_non_existing_user_filter(self):
        r = self.client.get(BASE_URL + '/trades/?user_id=123')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data, [])

    def test_with_user_and_type_buy_filters(self):
        r = self.client.get(BASE_URL + '/trades/?user_id=23&type=buy')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        without_ids = [strip_id(user) for user in data]
        expected_trades = [user23_buy_ABX]
        self.assertListEqual(without_ids, expected_trades)

    def test_with_user_and_type_sell_filters(self):
        r = self.client.get(BASE_URL + '/trades/?user_id=23&type=sell')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        without_ids = [strip_id(user) for user in data]
        expected_trades = [user23_sell_AAC]
        self.assertListEqual(without_ids, expected_trades)


class TestGetTradesById(TestCase):

    def setUp(self):
        self.client = RequestsClient()
        r = self.client.post(BASE_URL + '/trades/', json=user23_buy_ABX)
        try:
            self.stock_id = r.json()['id']
        except JSONDecodeError:
            self.fail("/trades/ endpoint for POST request not implemented correctly")

    def test_with_existing_id(self):
        r = self.client.get(BASE_URL + '/trades/' + str(self.stock_id))
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn('id', data)
        self.assertIsInstance(data['id'], int)
        self.assertDictEqual(strip_id(data), user23_buy_ABX)

    def test_with_non_existing_id(self):
        r = self.client.get(BASE_URL + '/trades/12333')
        self.assertEqual(r.status_code, 404)


class TestDeleteTradesById(TestCase):

    def setUp(self):
        self.client = RequestsClient()
        r = self.client.post(BASE_URL + '/trades/', json=user23_buy_ABX)
        try:
            self.stock_id = r.json()['id']
        except JSONDecodeError:
            self.fail("/trades/ endpoint for POST request not implemented correctly")

    def test_with_existing_id(self):
        r = self.client.delete(BASE_URL + '/trades/' + str(self.stock_id))
        self.assertEqual(r.status_code, 204)
        r1 = self.client.get(BASE_URL + '/trades/' + str(self.stock_id))
        self.assertEqual(r1.status_code, 404)

    def test_with_non_existing_id(self):
        r = self.client.delete(BASE_URL + '/trades/12333')
        self.assertEqual(r.status_code, 404)


class TestInvalidOperations(TestCase):

    def setUp(self):
        self.client = RequestsClient()
        r = self.client.post(BASE_URL + '/trades/', json=user23_buy_ABX)
        try:
            self.stock_id = r.json()['id']
        except JSONDecodeError:
            self.fail("/trades/ endpoint for POST request not implemented correctly")

    def test_put_not_allowed(self):
        r = self.client.put(BASE_URL + '/trades/' + str(self.stock_id), json=user23_buy_ABX)
        self.assertEqual(r.status_code, 405)

    def test_patch_not_allowed(self):
        r = self.client.patch(BASE_URL + '/trades/' + str(self.stock_id), json=user23_buy_ABX)
        self.assertEqual(r.status_code, 405)
