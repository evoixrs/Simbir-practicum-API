from requests import Response

from api_client import endpoints
from api_client.base_client import BaseClient


class EntityClient(BaseClient):
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
