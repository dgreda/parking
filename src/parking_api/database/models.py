from parking_api.database import db


class Rate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weekday = db.Column(db.Integer)
    time_from = db.Column(db.Time)
    time_to = db.Column(db.Time)
    timezone = db.Column(db.Text)
    price = db.Column(db.Integer)

    def __init__(self, weekday, time_from, time_to, timezone, price):
        self.weekday = weekday
        self.time_from = time_from
        self.time_to = time_to
        self.timezone = timezone
        self.price = price
