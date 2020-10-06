from parking_api.database import db
from parking_api.database.models import Rate


class RatesRepository(object):
    def get_all_rates(self):
        return Rate.query.all()

    def get_rates_timezone(self):
        rate = Rate.query.first()

        if rate is None:
            return None

        return rate.timezone

    def update_rates_in_db(self, rates):
        current_rates = self.get_all_rates()
        for current_rate in current_rates:
            db.session.delete(current_rate)

        for rate in rates:
            db.session.add(rate)

        db.session.commit()

    def find_rate(self, weekday, time_from, time_to):
        return Rate.query.filter(Rate.weekday == weekday, Rate.time_from <= time_from, Rate.time_to >= time_to).first()
