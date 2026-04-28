import json

import allure
from requests import Response


def attach_json(name: str, data: dict | list | None) -> None:
    allure.attach(
        json.dumps(data, ensure_ascii=False, indent=2),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )


def attach_request(
    method: str,
    url: str,
    payload: dict | None = None,
    params: dict | None = None,
) -> None:
    allure.attach(
        f"{method.upper()} {url}",
        name="HTTP request metadata",
        attachment_type=allure.attachment_type.TEXT,
    )

    if params:
        attach_json("Request query params", params)

    if payload:
        attach_json("Request body", payload)


def attach_response(response: Response) -> None:
    allure.attach(
        (
            f"{response.request.method} {response.url}\n"
            f"Status code: {response.status_code}\n"
            f"Content-Type: {response.headers.get('content-type', '')}"
        ),
        name="HTTP response metadata",
        attachment_type=allure.attachment_type.TEXT,
    )

    try:
        attach_json("Response body", response.json())
    except ValueError:
        allure.attach(
            response.text,
            name="Response body",
            attachment_type=allure.attachment_type.TEXT,
        )
