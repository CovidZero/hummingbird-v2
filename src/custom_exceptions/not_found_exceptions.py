from werkzeug.exceptions import HTTPException


class NotFoundException(HTTPException):
    """
    Base HTTPException for NOT FOUND - 404
    You should extend new classes in this file bellow
    and setup a custom description.
    The status code should remains the same
    """
    def __init__(self):
        super(HTTPException, self).__init__()
        self.code = 400
