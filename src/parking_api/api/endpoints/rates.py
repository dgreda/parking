import logging

from flask import request
from flask_restx import Resource
from parking_api.api.restx import api
from parking_api.api.serializers import rate, rates_collection, quote_request, quote
from parking_api.services.rates import RatesService

log = logging.getLogger(__name__)

ns = api.namespace('rates', description='Operations related to parking rates')

rates_service = RatesService()


@ns.route('/')
class RatesCollection(Resource):

    @api.response(204, 'Successfully updated rates.')
    @api.response(422, 'Unprocessable Entity')
    @api.expect(rates_collection)
    def put(self):
        """
        Updates available parking rates.

        Use this endpoint to update parking rates that will be used in parking quotes calculations.

        Send a JSON object representing new rates, e.g.:
        ```
        {
          "rates": [
            {
              "days": "mon,tues,thurs",
              "times": "0900-2100",
              "tz": "America/Chicago",
              "price": 1500
            },
            {
              "days": "fri,sat,sun",
              "times": "0900-2100",
              "tz": "America/Chicago",
              "price": 2000
            },
            {
              "days": "wed",
              "times": "0600-1800",
              "tz": "America/Chicago",
              "price": 1750
            },
            {
              "days": "mon,wed,sat",
              "times": "0100-0500",
              "tz": "America/Chicago",
              "price": 1000
            },
            {
              "days": "sun,tues",
              "times": "0100-0700",
              "tz": "America/Chicago",
              "price": 925
            }
          ]
        }
        ```
        """
        data = request.json

        parsed_rates = rates_service.parse_rates(data.get('rates'))
        rates_service.update_rates_in_db(parsed_rates)

        return None, 204


@ns.route('/quote')
class RatesCollection(Resource):

    @api.response(200, 'OK')
    @api.response(422, 'Unprocessable Entity')
    @api.expect(quote_request)
    @api.marshal_with(quote)
    def post(self):
        """
        Returns parking rate quote for requested datetimes.

        Send a JSON object like this:

        ```
        {
          "from": "2015-07-01T07:00:00-05:00",
          "to": "2015-07-01T12:00:00-05:00"
        }
        """
        data = request.json

        primary_timezone = rates_service.get_primary_timezone()
        rate = rates_service.find_rate(primary_timezone, data.get('from'), data.get('to'))

        if rate is not None:
            return {'rate': rate.price}, 200
        else:
            return {'rate': 'unavailable'}, 200
