import pytest
import json
import os


@pytest.mark.usefixtures('client_class')
class TestRatesEndpoint:

    def test_rates_submission_with_invalid_days(self):
        res = self.client.put('/api/rates/', json={
            "rates": [
                {
                    "days": "monoday,tues,thurs",
                    "times": "0900-2100",
                    "tz": "America/Chicago",
                    "price": 1500
                }
            ]
        })
        assert res.status_code == 422
        expected = {'message': 'Invalid day name: monoday'}
        assert expected == res.get_json()

    def test_rates_submission_with_invalid_times(self):
        invalid_times = "09001-2100"
        res = self.client.put('/api/rates/', json={
            "rates": [
                {
                    "days": "mon,tues,thurs",
                    "times": invalid_times,
                    "tz": "America/Chicago",
                    "price": 1500
                }
            ]
        })
        assert res.status_code == 422
        expected = {'message': 'Invalid times specified: ' + invalid_times}
        assert expected == res.get_json()

    def test_rates_submission_with_invalid_timezone(self):
        invalid_timezone = "Neverland/Neverland"
        res = self.client.put('/api/rates/', json={
            "rates": [
                {
                    "days": "mon,tues,thurs",
                    "times": "0900-2100",
                    "tz": invalid_timezone,
                    "price": 1500
                }
            ]
        })
        assert res.status_code == 422
        expected = {'message': 'Invalid Timezone string provided: ' + invalid_timezone}
        assert expected == res.get_json()

    def test_rates_submission_with_mixed_timezones(self):
        res = self.client.put('/api/rates/', json={
            "rates": [
                {
                    "days": "mon,tues,thurs",
                    "times": "0900-2100",
                    "tz": "America/Chicago",
                    "price": 1500
                },
                {
                    "days": "wed",
                    "times": "0900-2100",
                    "tz": "America/Toronto",
                    "price": 1500
                }
            ]
        })
        assert res.status_code == 422
        expected = {'message': 'Mixed timezone rates were provided. Please use the same timezone for rates submission'}
        assert expected == res.get_json()

    def test_successful_rates_submission(self, database):
        with open(os.path.dirname(__file__) + '/../fixtures/rates.json') as f:
            rates = json.load(f)
            res = self.client.put('/api/rates/', json=rates)

            assert res.status_code == 204

