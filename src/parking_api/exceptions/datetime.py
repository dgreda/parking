from parking_api.exceptions import ApiClientException

class InvalidTimezoneString(ApiClientException):
    def __init__(self, timezone, message="Invalid Timezone string provided: "):
        self.timezone = timezone
        self.message = message + timezone
        super().__init__(self.message)
