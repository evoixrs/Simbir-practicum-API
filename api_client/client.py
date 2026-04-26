import logging

from requests import Response, Session

from api_client import endpoints
from helpers.allure_helpers import attach_request, attach_response


logger = logging.getLogger("api_tests")


class EntityClient:
    def __init__(self, base_url: str, timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = Session()
        self.timeout = timeout

    def build_url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _send_request(
        self,
        method: str,
        path: str,
        payload: dict | None = None,
        params: dict | None = None,
    ) -> Response:
        url = self.build_url(path)
        logger.info("Request: %s %s", method.upper(), url)

        if params:
            logger.info("Query params: %s", params)

        if payload:
            logger.info("Request body: %s", payload)

        attach_request(
            method=method,
            url=url,
            payload=payload,
            params=params,
        )

        response = self.session.request(
            method=method,
            url=url,
            json=payload,
            params=params,
            timeout=self.timeout,
        )

        logger.info(
            "Response: %s %s",
            response.status_code,
            response.text,
        )
        attach_response(response)

        return response

    def post(self, path: str, payload: dict | None = None) -> Response:
        return self._send_request(
            method="POST",
            path=path,
            payload=payload,
        )

    def delete(self, path: str) -> Response:
        return self._send_request(
            method="DELETE",
            path=path,
        )

    def get(self, path: str, params: dict | None = None) -> Response:
        return self._send_request(
            method="GET",
            path=path,
            params=params,
        )

    def patch(self, path: str, payload: dict | None = None) -> Response:
        return self._send_request(
            method="PATCH",
            path=path,
            payload=payload,
        )

    def create_entity(self, payload: dict) -> Response:
        return self.post(path=endpoints.CREATE_ENTITY, payload=payload)

    def delete_entity(self, entity_id: int) -> Response:
        return self.delete(
            path=endpoints.DELETE_ENTITY.format(entity_id=entity_id),
        )

    def get_entity(self, entity_id: int) -> Response:
        return self.get(
            path=endpoints.GET_ENTITY.format(entity_id=entity_id),
        )

    def get_all_entities(self, params: dict | None = None) -> Response:
        return self.get(
            path=endpoints.GET_ALL_ENTITIES,
            params=params,
        )

    def patch_entity(self, entity_id: int, payload: dict) -> Response:
        return self.patch(
            path=endpoints.PATCH_ENTITY.format(entity_id=entity_id),
            payload=payload,
        )
