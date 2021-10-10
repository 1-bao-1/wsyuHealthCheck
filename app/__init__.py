from datetime import datetime
from .health_check import health_check
from . import constants


class InvalidRequestParamException(Exception):
    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message


def check_request_params(name: str, id: str):
    if not name or not id:
        raise InvalidRequestParamException(
            code=400, message=constants.NO_NAME_OR_ID_MESSAGE)

    if len(id) != 11 or len(name) > 5 or (int(id[:4]) < 2017 or int(id[:4]) > datetime.now().year):
        raise InvalidRequestParamException(
            code=400, message=constants.INVALID_NAME_OR_ID_MESSAGE)
