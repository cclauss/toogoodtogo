from rest_framework.test import APITestCase
from datetime import date, datetime

from stock_keeping.models import Shop, StockReading


class StockReadingTest(APITestCase):
    def test_stock_read_list_get(self):
        StockReading.objects.create(GTIN='YOP CHOCO', expiry='2022-03-26', occurrence='2022-02-23 12:00:01Z')
        StockReading.objects.create(GTIN='MADELEINE', expiry='2022-03-24', occurrence='2022-02-23 12:00:01Z')

        resp = self.client.get('/api/stock_keeping/')
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(resp.content, [
        {'GTIN': 'MADELEINE', 'expiry': '2022-03-24', 'occurrence': '2022-02-23T12:00:01Z'},
        {'GTIN': 'YOP CHOCO', 'expiry': '2022-03-26', 'occurrence': '2022-02-23T12:00:01Z'},
        ])

    def test_stock_read_list_post(self):
        data = {'GTIN': 'YOP CHOCO', 'expiry': '2022-03-27', 'occurrence': '2022-02-23 12:55:12Z'}
        resp = self.client.post('/api/stock_keeping/', data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(StockReading.objects.count(), 1)
        stock_reading = StockReading.objects.get()
        self.assertEqual(stock_reading.GTIN, data['GTIN'])
        self.assertEqual(stock_reading.expiry, date.fromisoformat(data['expiry']))
        self.assertEqual(stock_reading.occurrence, datetime.fromisoformat(data['occurrence']))

    def test_stock_read_batch_post(self):
        resp = self.client.post('/api/stock_keeping/batch/', [
            {'GTIN': 'YOP CHOCO', 'expiry': '2022-03-27', 'occurrence': '2022-02-23 12:55:12Z'},
            {'GTIN': 'MADELEINE', 'expiry': '2022-03-25', 'occurrence': '2022-02-23 12:55:12Z'},
        ])
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(StockReading.objects.count(), 2)

    def test_conflicting_stock_read_post(self):
        resp1 = self.client.post('/api/stock_keeping/batch/', [
            {'GTIN': 'MADELEINE', 'expiry': '2022-03-01', 'occurrence': '2022-02-23 12:00:00Z'},
            {'GTIN': 'YOP CHOCO', 'expiry': '2022-03-01', 'occurrence': '2022-02-23 12:00:00Z'},
        ])
        self.assertEqual(resp1.status_code, 201)
        resp2 = self.client.post('/api/stock_keeping/batch/', [
            {'GTIN': 'MADELEINE', 'expiry': '2022-03-03', 'occurrence': '2022-02-24 14:00:00Z'},
            {'GTIN': 'YOP CHOCO', 'expiry': '2022-03-03', 'occurrence': '2022-02-24 14:00:00Z'},
        ])
        self.assertEqual(resp2.status_code, 201)

        resp3 = self.client.get('/api/stock_keeping/')
        self.assertEqual(resp3.status_code, 200)
        self.assertEqual(resp3.json(), [
            {'GTIN': 'MADELEINE', 'expiry': '2022-03-03', 'occurrence': '2022-02-24T14:00:00Z'},
            {'GTIN': 'YOP CHOCO', 'expiry': '2022-03-03', 'occurrence': '2022-02-24T14:00:00Z'},
        ])
