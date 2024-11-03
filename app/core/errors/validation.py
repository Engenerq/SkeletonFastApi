from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_definition
from pydantic import ValidationError


async def validation_error_handler(
        _request: Request,
        exc: RequestValidationError | ValidationError,

) -> JSONResponse:
    return JSONResponse(
        {"errors": exc.errors()},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


validation_error_definition["properties"] = {
    "errors": {
        "title": "errors",
        "type": "array",
        "items": {"$ref": f"{REF_PREFIX}ValidationError"}
    }
}


async def http_errors_handler(
        _request: Request,
        exc: HTTPException,
) -> JSONResponse:
    return JSONResponse(
        {"errors": [exc.detail]},
        status_code=exc.status_code,

    )
