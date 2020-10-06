from flask_restx import fields
from parking_api.api.restx import api

rate = api.model('Rate', {
    'days': fields.String(required=True, description='Rate validity days, e.g. "fri,sat,sun"'),
    'times': fields.String(required=True, description='Rate validity times, e.g. "0900-2100"'),
    'tz': fields.String(required=True, description='Rate validity timezone, e.g. "America/Chicago"'),
    'price': fields.Integer(required=True, description='Rate price, e.g. 2000'),
})

rates_collection = api.model('RatesCollection', {
    'rates': fields.List(fields.Nested(rate))
})

quote_request = api.model('QuoteRequest', {
    'from': fields.DateTime(required=True, description='Timezone aware ISO-8601 datetime, e.g.: "2015-07-01T07:00:00-05:00"'),
    'to': fields.DateTime(required=True, description='Timezone aware ISO-8601 datetime, e.g.: "2015-07-01T12:00:00-05:00"'),
})

quote = api.model('Quote', {
    'rate': fields.Raw(required=True),
})
