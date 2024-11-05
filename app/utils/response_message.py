from email.policy import default
from typing import Any

from utils.types_utils.response_types import ResponseMessageT, ResponseT


def responseMessage(data: ResponseT) -> ResponseMessageT:
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
