from http import HTTPStatus

import allure

from api_client.client import EntityClient
from api_client.models.entity import EntityResponse
from helpers.assert_helpers import (
    assert_content_type,
    assert_entities_contain_ids,
    assert_entity_matches_payload,
    assert_status_code,
)
from helpers.response_helpers import deserialize_entity_filter
from tests.conftest import CreatedEntity


def find_entity_by_id(entities: list[EntityResponse], entity_id: int) -> EntityResponse:
    for entity in entities:
        if entity.id == entity_id:
            return entity

    raise AssertionError(f"Entity with id '{entity_id}' not found")


@allure.feature("Сущности")
@allure.story("Получение списка сущностей")
@allure.suite("API tests")
@allure.sub_suite("Entity CRUD")
@allure.tag("api", "crud", "positive", "TC-04")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC-04: Получение списка сущностей через GET /api/getAll")
@allure.description(
    "Проверка получения списка сущностей по тест-кейсу TC-04 из docs/test_cases.md. "
    "Перед тестом создаются две сущности, затем тест запрашивает список через "
    "GET /api/getAll с query-параметрами и проверяет наличие созданных сущностей."
)
def test_get_all_entities(
    api_client: EntityClient,
    created_entities: list[CreatedEntity],
) -> None:
    params = {
        "verified": True,
        "page": 1,
        "perPage": 10,
    }
    expected_ids = [entity.entity_id for entity in created_entities]

    with allure.step("Отправить GET /api/getAll с query-параметрами"):
        get_all_response = api_client.get_all_entities(params=params)
        assert_status_code(get_all_response, HTTPStatus.OK)
        assert_content_type(get_all_response, "application/json")

    with allure.step("Десериализовать Response body в объект EntityFilterResponse"):
        entity_filter = deserialize_entity_filter(get_all_response)

    with allure.step("Проверить параметры пагинации"):
        assert entity_filter.page == params["page"], (
            f"Expected page '{params['page']}', got '{entity_filter.page}'"
        )
        assert entity_filter.per_page == params["perPage"], (
            f"Expected perPage '{params['perPage']}', got '{entity_filter.per_page}'"
        )

    with allure.step("Найти созданные сущности в списке entity по id"):
        assert_entities_contain_ids(
            entities=entity_filter.entity,
            expected_ids=expected_ids,
        )

    with allure.step("Проверить данные найденных сущностей"):
        for created_entity in created_entities:
            entity = find_entity_by_id(
                entities=entity_filter.entity,
                entity_id=created_entity.entity_id,
            )
            assert entity.verified is True, (
                f"Expected verified to be True, got '{entity.verified}'"
            )
            assert_entity_matches_payload(
                entity=entity,
                payload=created_entity.payload,
            )
