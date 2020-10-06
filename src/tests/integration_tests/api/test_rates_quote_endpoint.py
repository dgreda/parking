import pytest
import json
import os


@pytest.mark.usefixtures('client_class')
class TestRatesQuoteEndpoint:
    QUOTE_ENDPOINT = '/api/rates/quote'

    def test_invalid_quote_requests(self):
        invalid_date = 'textthatisclearlynotadate+00:00'
        res = self.client.post(self.QUOTE_ENDPOINT, json={
            'from': invalid_date,
            'to': '2015-07-01T12:00:00-05:00'
        })
        assert res.status_code == 422
        assert {'message': "Invalid 'from' date specified: " + invalid_date} == res.get_json()

        invalid_date = '2015-07-01Tgarbage12:00:00-05:00'
        res = self.client.post(self.QUOTE_ENDPOINT, json={
            'from': '2015-07-01T12:00:00-05:00',
            'to': invalid_date
        })
        assert res.status_code == 422
        assert {'message': "Invalid 'to' date specified: " + invalid_date} == res.get_json()

    def test_quotes(self, database):
        with open(os.path.dirname(__file__) + '/../fixtures/rates.json') as f:
            rates = json.load(f)
            res = self.client.put('/api/rates/', json=rates)
            assert res.status_code == 204

            res = self.client.post(self.QUOTE_ENDPOINT, json={
                'from': '2015-07-01T07:00:00-05:00',
                'to': '2015-07-01T12:00:00-05:00'
            })
            assert res.status_code == 200
            assert {'rate': 1750} == res.get_json()

            res = self.client.post(self.QUOTE_ENDPOINT, json={
                'from': '2015-07-04T15:00:00+00:00',
                'to': '2015-07-04T20:00:00+00:00'
            })
            assert res.status_code == 200
            assert {'rate': 2000} == res.get_json()

            res = self.client.post(self.QUOTE_ENDPOINT, json={
                'from': '2015-07-04T07:00:00+05:00',
                'to': '2015-07-04T20:00:00+05:00'
            })
            assert res.status_code == 404
            assert {'rate': 'unavailable'} == res.get_json()
