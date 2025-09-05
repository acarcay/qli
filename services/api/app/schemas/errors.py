from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorDetail


# Common error codes
class ErrorCodes:
    NOT_FOUND = "QL-4041"
    VALIDATION_ERROR = "QL-4001"
    INTERNAL_ERROR = "QL-5001"
