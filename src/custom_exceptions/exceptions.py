from werkzeug.exceptions import HTTPException


class BaseError(HTTPException):

    def __init__(self, description):
        super(HTTPException, self).__init__()
        self.description = description


class BadRequest(BaseError):
    code = 400


class NotFound(BaseError):
    code = 404


class ServerError(BaseError):
    code = 500
