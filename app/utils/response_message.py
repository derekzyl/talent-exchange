from email.policy import default
from typing import Any

from utils.types_utils.response_types import ResponseMessageT, ResponseT


def responseMessage(data: ResponseT) -> ResponseMessageT:
    """
    The function responseMessage returns a response message based on the success status in the input
    data.
    
    :param data: The `responseMessage` function takes a dictionary `data` as input, which is expected to
    have the following keys:
    :type data: ResponseT
    """
    match (data["success_status"]):
        case True:
            return {
                "message": data["message"],
                "success": data["success_status"],
                "data": data["data"],
            }
        case False:
            return {
                "message": data["message"],
                "success": data["success_status"],
                "error": data["data"],
            }
