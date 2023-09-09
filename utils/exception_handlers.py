from enum import Enum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

class ErrorEnum(Enum):
    ERR_001 = (
        "Validation Error",
        status.HTTP_400_BAD_REQUEST,
        "The request data failed validation. Please check your input and try again.",
    )
    ERR_002 = (
        "Authentication Error",
        status.HTTP_401_UNAUTHORIZED,
        "Authentication credentials were not provided.",
    )
    ERR_003 = (
        "Internal Server Error",
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "Something went wrong on our end. Please try again later.",
    )
    ERR_004 = (
        "Permission Error",
        status.HTTP_403_FORBIDDEN,
        "Authentication credentials are either missing or the user lacks the necessary permissions to perform this action.",
    )
    ERR_005 = (
        "Invalid Request Method",
        status.HTTP_405_METHOD_NOT_ALLOWED,
        "Accessing the resource with an unsupported method.",
    )

class ErrorResponse(Response):
    def __init__(
        self,
        code: ErrorEnum,
        serializer_errors: dict = None,
        extra_detail: str = None,
        status: int = None,
        headers: dict = None,
    ):
        super().__init__(None, status=status or code.value[1])

        error_data = {
            "error_code": code.name,
            "error": code.value[0],
            "detail": [
                {"loc": ["body", field], "msg": error[0], "type": error[0].code}
                for field, error in serializer_errors.items()
            ] if serializer_errors else code.value[2],
        }

        if extra_detail:
            error_data["extra_detail"] = extra_detail

        self.data = error_data

        if headers:
            for name, value in headers.items():
                self[name] = value

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response:
        result = [code for code in ErrorEnum if code.value[1] == response.status_code]

        custom_response = ErrorResponse(code=result[0], status=response.status_code)
        return custom_response
    response
