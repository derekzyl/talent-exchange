from typing import Any, Dict


def create_response_message[T](
    success: bool,
    message: str,
    data: T|None = None,
    doc_length: int = None,
    error: Any = None,
    stack: Any = None,
    config: str = "production"
) -> Dict[str, Any]:
    """Create standardized response message"""
    if success:
        response = {
            "message": message,
            "data": data,
            "success": success
        }
        if doc_length is not None:
            response["doc_length"] = doc_length
        return response
    else:
        response = {
            "message": message,
            "error": error,
            "success": success
        }
        if config == "development" and stack:
            response["stack"] = stack
        return response