from datetime import date, datetime

from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient

from stock_keeping.models import Shop, StockReading, Profile


class StockReadingTest(APITestCase):
    def setUp(self):
        self.shop = Shop.objects.create(name='A2Pas Nation')

        # I wish we could do it in one line, but I have no idea how to do it elegantly
        self.user = User.objects.create_user('john', password='passoire')
        self.user.profile.shop = self.shop

        self.client.force_authenticate(user=self.user)

    def test_stock_read_get_list(self):
        StockReading.objects.create(GTIN='YOP CHOCO', expires_at='2022-03-26', scanned_at='2022-02-23 12:00:01Z',
                                    shop=self.shop)
        StockReading.objects.create(GTIN='MADELEINE', expires_at='2022-03-24', scanned_at='2022-02-23 12:00:01Z',
                                    shop=self.shop)

        resp = self.client.get('/api/stock_reading/')
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(resp.content, [
            {'GTIN': 'MADELEINE', 'expires_at': '2022-03-24', 'scanned_at': '2022-02-23T12:00:01Z'},
            {'GTIN': 'YOP CHOCO', 'expires_at': '2022-03-26', 'scanned_at': '2022-02-23T12:00:01Z'},
        ])

    def test_stock_read_post(self):
        data = {'GTIN': 'YOP CHOCO', 'expires_at': '2022-03-27', 'scanned_at': '2022-02-23 12:55:12Z'}
        resp = self.client.post('/api/stock_reading/', data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(StockReading.objects.count(), 1)
        stock_reading = StockReading.objects.get()
        self.assertEqual(stock_reading.GTIN, data['GTIN'])
        self.assertEqual(stock_reading.expires_at, date.fromisoformat(data['expires_at']))
        self.assertEqual(stock_reading.scanned_at, datetime.fromisoformat(data['scanned_at']))

    def test_stock_read_batch_post(self):
        resp = self.client.post('/api/stock_reading/batch/', [
            {'GTIN': 'YOP CHOCO', 'expires_at': '2022-03-27', 'scanned_at': '2022-02-23 12:55:12Z'},
            {'GTIN': 'MADELEINE', 'expires_at': '2022-03-25', 'scanned_at': '2022-02-23 12:55:12Z'},
        ])
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(StockReading.objects.count(), 2)

    def test_stock_read_conflicting_batch_post(self):
        resp1 = self.client.post('/api/stock_reading/batch/', [
            {'GTIN': 'MADELEINE', 'expires_at': '2022-03-01', 'scanned_at': '2022-02-23 12:00:00Z'},
            {'GTIN': 'YOP CHOCO', 'expires_at': '2022-03-01', 'scanned_at': '2022-02-23 12:00:00Z'},
        ])
        self.assertEqual(resp1.status_code, 201)
        resp2 = self.client.post('/api/stock_reading/batch/', [
            {'GTIN': 'MADELEINE', 'expires_at': '2022-03-03', 'scanned_at': '2022-02-24 14:00:00Z'},
            {'GTIN': 'YOP CHOCO', 'expires_at': '2022-03-03', 'scanned_at': '2022-02-24 14:00:00Z'},
        ])
        self.assertEqual(resp2.status_code, 201)

        resp3 = self.client.get('/api/stock_reading/')
        self.assertEqual(resp3.status_code, 200)
        self.assertEqual(resp3.json(), [
            {'GTIN': 'MADELEINE', 'expires_at': '2022-03-03', 'scanned_at': '2022-02-24T14:00:00Z'},
            {'GTIN': 'YOP CHOCO', 'expires_at': '2022-03-03', 'scanned_at': '2022-02-24T14:00:00Z'},
        ])

    def test_stock_read_get_list_multi_user(self):
        user2 = User.objects.create(username='paul', password='pablo')
        shop2 = Shop.objects.create(name='Franprix rue Montreuil')

        # I still don't know how to do it in one line
        user2.profile.shop = shop2

        # create a second API client for user2 (we can't use self.client because it's already authenticated)
        client2 = APIClient()
        client2.force_authenticate(user=user2)
        # just for consistency
        client1 = self.client

        # create a stock reading as user1
        data1 = {'GTIN': 'YOP CHOCO', 'expires_at': '2022-03-27', 'scanned_at': '2022-02-23T12:55:12Z'}
        resp1 = client1.post('/api/stock_reading/', data1)
        self.assertEqual(resp1.status_code, 201)

        # create a stock reading as user2
        data2 = {'GTIN': 'COCA ZERO', 'expires_at': '2022-03-27', 'scanned_at': '2022-02-23T12:55:12Z'}
        resp2 = client2.post('/api/stock_reading/', data2)
        self.assertEqual(resp2.status_code, 201)

        # check each user can only see their own stock readings
        resp3 = client1.get('/api/stock_reading/')
        self.assertEqual(resp3.status_code, 200)
        self.assertEqual(resp3.json(), [data1])

        resp4 = client2.get('/api/stock_reading/')
        self.assertEqual(resp4.status_code, 200)
        self.assertEqual(resp4.json(), [data2])

    def test_stock_read_get_list_scanned_at_greater_than(self):
        StockReading.objects.create(GTIN='YOP CHOCO', expires_at='2022-03-26', scanned_at='2022-02-23 12:00:00Z',
                                    shop=self.shop)
        StockReading.objects.create(GTIN='MADELEINE', expires_at='2022-03-27', scanned_at='2022-02-24 12:00:00Z',
                                    shop=self.shop)
        StockReading.objects.create(GTIN='COCA ZERO', expires_at='2022-03-28', scanned_at='2022-02-25 12:00:00Z',
                                    shop=self.shop)
        StockReading.objects.create(GTIN='DANETTE VAN', expires_at='2022-03-29', scanned_at='2022-02-26 12:00:00Z',
                                    shop=self.shop)

        resp = self.client.get('/api/stock_reading/?scanned_at__gt=2022-02-24T12:01:00Z')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), [
            {'GTIN': 'COCA ZERO', 'expires_at': '2022-03-28', 'scanned_at': '2022-02-25T12:00:00Z'},
            {'GTIN': 'DANETTE VAN', 'expires_at': '2022-03-29', 'scanned_at': '2022-02-26T12:00:00Z'},
        ])
