from parking_api.exceptions import ApiException


class MixedTimezonesInRates(ApiException):
    def __init__(self, message="Mixed timezone rates were provided. Please use the same timezone for rates submission"):
        self.message = message
        super().__init__(self.message)
