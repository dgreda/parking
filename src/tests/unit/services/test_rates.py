from parking_api.exceptions import ApiException
from parking_api.services.rates import RatesService
from unittest.mock import MagicMock
import pytest


@pytest.fixture
def rates_service():
    return RatesService(MagicMock())


class TestRates:

    def test_find_rate_throws_exception_on_invalid_date(self, rates_service):
        with pytest.raises(ApiException):
            rates_service.find_rate('America/Chicago', 'garbage', '2020-09-01T12:00:00-05:00')
        with pytest.raises(ApiException):
            rates_service.find_rate('America/Chicago', '2020-09-01T12:00:00-05:00', '2020-09-01T12:00:00-05:00wrong')

    def test_find_rate(self, rates_service):
        repo_mock = MagicMock()
        repo_mock.find_rate.return_value = None
        rates_service.repository = repo_mock

        res = rates_service.find_rate('America/Chicago', '2020-10-05T10:00:00-06:00', '2020-10-05T14:00:00-06:00')

        assert res is None
