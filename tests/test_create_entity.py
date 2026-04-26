import logging

import allure

from api_client.client import EntityClient
from api_client.payloads.entity import create_entity_payload
from helpers.assert_helpers import (
    assert_content_type,
    assert_entity_has_ids,
    assert_entity_matches_payload,
    assert_status_code,
)
from helpers.response_helpers import deserialize_entity, get_created_entity_id


logger = logging.getLogger("api_tests")


@allure.feature("Сущности")
@allure.story("Создание сущности")
@allure.title("Создание сущности через POST /api/create")
def test_create_entity(api_client: EntityClient) -> None:
    payload = create_entity_payload()
    entity_id = None

    try:
        with allure.step("Отправить POST /api/create с валидным телом запроса"):
            create_response = api_client.create_entity(
                payload=payload.model_dump(exclude_none=True),
            )
            assert_status_code(create_response, 200)
            assert_content_type(create_response, "text/plain; charset=utf-8")
            entity_id = get_created_entity_id(create_response)

        with allure.step("Получить созданную сущность через GET /api/get/{id}"):
            get_response = api_client.get_entity(entity_id=entity_id)
            assert_status_code(get_response, 200)
            assert_content_type(get_response, "application/json")

        with allure.step("Десериализовать Response body в объект EntityResponse"):
            entity = deserialize_entity(get_response)

        with allure.step("Проверить данные созданной сущности"):
            assert entity.id == entity_id, (
                f"Expected entity id '{entity_id}', got '{entity.id}'"
            )
            assert_entity_has_ids(entity)
            assert_entity_matches_payload(entity=entity, payload=payload)
    finally:
        if entity_id is not None:
            with allure.step("Удалить созданную тестовую сущность"):
                delete_response = api_client.delete_entity(entity_id=entity_id)
                if delete_response.status_code != 204:
                    logger.warning(
                        "Failed to delete test entity %s. Status: %s. Body: %s",
                        entity_id,
                        delete_response.status_code,
                        delete_response.text,
                    )
