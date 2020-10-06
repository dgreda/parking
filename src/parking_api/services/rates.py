from parking_api.database import db
from parking_api.database.models import Rate
from parking_api.exceptions import ApiException
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
            if bool(re.match("^\d{4}\-\d{4}$", raw_times)) is False:
                raise ApiException(f"Invalid times specified: {raw_times}")
            times = [r[:2] + ':' + r[2:] + ':00' for r in raw_times.split('-')]
            for day in days:
                if day not in days_of_week:
                    raise ApiException(f"Invalid day name: {day}")
                new_rate = Rate(days_of_week[day], times[0], times[1], timezone, rate.get('price'))
                parsed_rates.append(new_rate)
            last_timezone = timezone

        return parsed_rates

    def update_rates_in_db(self, new_rates):
        current_rates = Rate.query.all()
        for current_rate in current_rates:
            db.session.delete(current_rate)

        for rate in new_rates:
            db.session.add(rate)

        db.session.commit()

    def get_all_rates(self):
        return Rate.query.all()

    def get_primary_timezone(self):
        rate = Rate.query.first()

        return rate.timezone

    def find_rate(self, target_tz: str, date_from: str, date_to: str) -> Optional[Rate]:
        try:
            date_from_in_target_tz = datetime_service.parse_iso8601_date_to_target_timezone(date_from, target_tz)
        except ValueError:
            raise ApiException(f"Invalid 'from' date specified: {date_from}")
        try:
            date_to_in_target_tz = datetime_service.parse_iso8601_date_to_target_timezone(date_to, target_tz)
        except ValueError:
            raise ApiException(f"Invalid 'to' date specified: {date_to}")

        if (date_from_in_target_tz.year != date_to_in_target_tz.year
                or date_from_in_target_tz.month != date_to_in_target_tz.month
                or date_from_in_target_tz.day != date_to_in_target_tz.day
        ):
            return None

        weekday = date_from_in_target_tz.weekday()
        time_from = date_from_in_target_tz.strftime('%H:%M')
        time_to = date_to_in_target_tz.strftime('%H:%M')

        return Rate.query.filter(Rate.weekday == weekday, Rate.time_from <= time_from, Rate.time_to >= time_to).first()
