from rest_framework import status
from rest_framework.exceptions import APIException


class BaseBookAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Произошла ошибка, связанная с книгой.'

    def __init__(self, detail=None):
        if detail is None:
            detail = self.default_detail
        self.detail = detail
        super().__init__(detail)
