from werkzeug.exceptions import HTTPException


class BadRequestException(HTTPException):
    """
    Base HTTPException for BAD REQUEST - 400
    You should extend new classes in this file bellow
    and setup a custom description.
    The status code should remains the same
    """
    def __init__(self):
        super(HTTPException, self).__init__()
        self.code = 400
