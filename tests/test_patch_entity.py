from http import HTTPStatus

import allure

from api_client.client import EntityClient
from api_client.payloads.entity import patch_entity_payload
from helpers.assert_helpers import (
    assert_content_type,
    assert_entity_matches_payload,
    assert_response_has_header,
    assert_status_code,
)
from helpers.response_helpers import deserialize_entity
from tests.conftest import CreatedEntity


@allure.feature("Сущности")
@allure.story("Обновление сущности")
@allure.suite("API tests")
@allure.sub_suite("Entity CRUD")
@allure.tag("api", "crud", "positive", "TC-05")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC-05: Обновление сущности через PATCH /api/patch/{id}")
@allure.description(
    "Проверка обновления сущности по тест-кейсу TC-05 из docs/test_cases.md. "
    "Перед тестом создается сущность, затем тест обновляет ее через PATCH /api/patch/{id} "
    "и проверяет обновленные данные через GET /api/get/{id}."
)
def test_patch_entity(
    api_client: EntityClient,
    created_entity: CreatedEntity,
) -> None:
    payload = patch_entity_payload()

    with allure.step("Отправить PATCH /api/patch/{id}"):
        patch_response = api_client.patch_entity(
            entity_id=created_entity.entity_id,
            payload=payload.model_dump(exclude_none=True),
        )
        assert_status_code(patch_response, HTTPStatus.NO_CONTENT)
        assert_response_has_header(patch_response, "date")

    with allure.step("Получить обновленную сущность через GET /api/get/{id}"):
        get_response = api_client.get_entity(entity_id=created_entity.entity_id)
        assert_status_code(get_response, HTTPStatus.OK)
        assert_content_type(get_response, "application/json")

    with allure.step("Десериализовать Response body в объект EntityResponse"):
        entity = deserialize_entity(get_response)

    with allure.step("Проверить обновленные данные сущности"):
        assert entity.id == created_entity.entity_id, (
            f"Expected entity id '{created_entity.entity_id}', got '{entity.id}'"
        )
        assert_entity_matches_payload(entity=entity, payload=payload)
