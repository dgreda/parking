import logging
import traceback

from parking_api.config import config
from parking_api.exceptions import ApiException, ApiClientException
from flask_restx import Api

log = logging.getLogger(__name__)

api = Api(version='1.0', title='Parking Quote API',
          description='API for retrieving parking quotes')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not config.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(ApiClientException)
def api_client_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': e.message}, 422


@api.errorhandler(ApiException)
def api_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': e.message}, 500
