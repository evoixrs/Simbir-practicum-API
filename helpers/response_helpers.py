from requests import Response

from api_client.models.entity import EntityFilterResponse, EntityResponse


def get_created_entity_id(response: Response) -> int:
    try:
        entity_id = int(response.text)
    except ValueError as exc:
        raise AssertionError(
            f"Expected response body with entity id, got '{response.text}'"
        ) from exc

    assert entity_id > 0, f"Expected positive entity id, got '{entity_id}'"
    return entity_id


def deserialize_entity(response: Response) -> EntityResponse:
    return EntityResponse.model_validate(response.json())


def deserialize_entity_filter(response: Response) -> EntityFilterResponse:
    return EntityFilterResponse.model_validate(response.json())
