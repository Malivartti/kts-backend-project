from aiohttp.web import json_response as aiohttp_json_response
from aiohttp.web_response import Response


def json_response(
    http_status: int = 200, status: str = "ok", data: dict | None = None
) -> Response:
    if data is None:
        data = {}

    return aiohttp_json_response(
        status=http_status,
        data={
            "status": status,
            "data": data,
        },
    )


def error_json_response(
    http_status: int,
    status: str = "error",
    message: str | None = None,
    data: dict | None = None,
):
    return aiohttp_json_response(
        status=http_status,
        data={"status": status, "message": str(message), "data": data or {}},
    )
