import allure
import pytest

from api_client.client import EntityClient
from helpers.assert_helpers import (
    assert_content_type,
    assert_entity_matches_payload,
    assert_status_code,
)
from helpers.response_helpers import deserialize_entity
from tests.conftest import CreatedEntity


pytestmark = pytest.mark.xdist_group("api_crud")


@allure.feature("Сущности")
@allure.story("Получение сущности")
@allure.title("Получение сущности через GET /api/get/{id}")
def test_get_entity(
    api_client: EntityClient,
    created_entity: CreatedEntity,
) -> None:
    with allure.step("Отправить GET /api/get/{id}"):
        get_response = api_client.get_entity(entity_id=created_entity.entity_id)
        assert_status_code(get_response, 200)
        assert_content_type(get_response, "application/json")

    with allure.step("Десериализовать Response body в объект EntityResponse"):
        entity = deserialize_entity(get_response)

    with allure.step("Проверить идентификатор сущности"):
        assert entity.id == created_entity.entity_id, (
            f"Expected entity id '{created_entity.entity_id}', got '{entity.id}'"
        )

    with allure.step("Проверить данные сущности"):
        assert_entity_matches_payload(
            entity=entity,
            payload=created_entity.payload,
        )
