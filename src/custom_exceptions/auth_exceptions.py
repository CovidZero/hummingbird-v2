from werkzeug.exceptions import HTTPException


class UnauthorizedError(HTTPException):

    def __init__(self):
        super(HTTPException, self).__init__()
        self.code = 401


class BadUsernameOrPassword(UnauthorizedError):
    description = 'Bad username or password'
