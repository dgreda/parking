from parking_api.exceptions import ApiClientException


class MixedTimezonesInRates(ApiClientException):
    def __init__(self, message="Mixed timezone rates were provided. Please use the same timezone for rates submission"):
        self.message = message
        super().__init__(self.message)
