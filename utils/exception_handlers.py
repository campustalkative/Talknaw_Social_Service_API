from rest_framework.response import Response
from typing import Any
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response




def ErrorResponse(message, errors):

    error_response_data = {
        "status_code": 400,
        "error": message, 
        "detail": [
            {
            "loc": [
                "body",
                field
            ],
            "msg": error[0],
            "type": error[0].code
            }
            for field, error in errors.items()
        ]
    }
    return error_response_data
