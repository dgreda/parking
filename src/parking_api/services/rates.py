from parking_api.database.models import Rate
from parking_api.exceptions import ApiException, ApiClientException
from parking_api.exceptions.rates import MixedTimezonesInRates
from parking_api.exceptions.datetime import InvalidTimezoneString
from parking_api.services.datetime import DateTimeService
from typing import Optional
import re
import pytz

days_of_week = {
    'mon': 0,
    'tues': 1,
    'wed': 2,
    'thurs': 3,
    'fri': 4,
    'sat': 5,
    'sun': 6
}

datetime_service = DateTimeService()


class RatesService(object):

    def __init__(self, repository):
        self.repository = repository

    def parse_rates(self, rates):
        parsed_rates = []
        last_timezone = None
        for rate in rates:
            timezone = rate.get('tz')
            if timezone not in pytz.all_timezones:
                raise InvalidTimezoneString(timezone)
            if last_timezone is not None and last_timezone != timezone:
                raise MixedTimezonesInRates
            days = rate.get('days').split(',')
            raw_times = rate.get('times')
            if bool(re.match(r'^\d{4}\-\d{4}$', raw_times)) is False:
                raise ApiClientException(f"Invalid times specified: {raw_times}")
            times = [r[:2] + ':' + r[2:] + ':00' for r in raw_times.split('-')]
            for day in days:
                if day not in days_of_week:
                    raise ApiClientException(f"Invalid day name: {day}")
                new_rate = Rate(days_of_week[day], times[0], times[1], timezone, rate.get('price'))
                parsed_rates.append(new_rate)
            last_timezone = timezone

        return parsed_rates

    def update_rates_in_db(self, new_rates):
        self.repository.update_rates_in_db(new_rates)

    def get_all_rates(self):
        return self.repository.get_all_rates()

    def get_primary_timezone(self):
        primary_timezone = self.repository.get_rates_timezone()

        if primary_timezone is None:
            raise ApiException('There are no rates available!')

        return primary_timezone

    def find_rate(self, target_tz: str, date_from: str, date_to: str) -> Optional[Rate]:
        try:
            date_from_in_target_tz = datetime_service.parse_iso8601_date_to_target_timezone(date_from, target_tz)
        except ValueError:
            raise ApiClientException(f"Invalid 'from' date specified: {date_from}")
        try:
            date_to_in_target_tz = datetime_service.parse_iso8601_date_to_target_timezone(date_to, target_tz)
        except ValueError:
            raise ApiClientException(f"Invalid 'to' date specified: {date_to}")

        if (date_from_in_target_tz.year != date_to_in_target_tz.year
                or date_from_in_target_tz.month != date_to_in_target_tz.month
                or date_from_in_target_tz.day != date_to_in_target_tz.day
        ):
            return None

        weekday = date_from_in_target_tz.weekday()
        time_from = date_from_in_target_tz.strftime('%H:%M')
        time_to = date_to_in_target_tz.strftime('%H:%M')

        return self.repository.find_rate(weekday, time_from, time_to)
