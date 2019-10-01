class FarmosAPIError(Exception):
    data = {}
    code = -1
    message = "An unknown error occurred"

    def __init__(self, message=None, code=None, data=None, response=None):
        if message:
            self.message = message
        if code:
            self.code = code
        if data:
            self.data = data

    def __str__(self):
        if self.code:
            return '{}: {}'.format(self.code, self.message)
        return self.message


class NotAuthenticatedError(FarmosAPIError):
    message = "APISession not authenticated before the request was made." \
              "Call farm.authenticate() before making requests."
    pass
