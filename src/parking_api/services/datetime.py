from datetime import datetime
from dateutil import parser
from pytz import timezone


class DateTimeService(object):
    def parse_iso8601_date_to_target_timezone(self, datetime: str, target_timezone: str) -> datetime:
        datetime_obj = parser.parse(datetime)
        datetime_obj_in_target_tz = datetime_obj.astimezone(timezone(target_timezone))

        return datetime_obj_in_target_tz
