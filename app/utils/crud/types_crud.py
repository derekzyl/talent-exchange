from typing import Any, TypedDict


class ResponseMessage( TypedDict, total=False):
    success_status: bool
    message: str
    error: Any
    data: Any
    doc_length: int|None


def response_message(success_status: bool, message: str, error: Any|None=None, data: Any| None=None, doc_length: int|None=None) -> ResponseMessage:
    if success_status:
        return {
            "success_status": success_status,
            "message": message,
            "data": data,
            "doc_length": doc_length
        }
    else:
        return {
            "success_status": success_status,
            "message": message,
            "error": str(error),
            "doc_length": doc_length
        }
