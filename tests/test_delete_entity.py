import allure
import pytest

from api_client.client import EntityClient
from helpers.assert_helpers import assert_response_has_header, assert_status_code
from tests.conftest import CreatedEntity


pytestmark = pytest.mark.xdist_group("api_crud")


@allure.feature("Сущности")
@allure.story("Удаление сущности")
@allure.title("Удаление сущности через DELETE /api/delete/{id}")
def test_delete_entity(
    api_client: EntityClient,
    created_entity: CreatedEntity,
) -> None:
    with allure.step("Отправить DELETE /api/delete/{id}"):
        delete_response = api_client.delete_entity(
            entity_id=created_entity.entity_id,
        )
        created_entity.is_deleted = True

    with allure.step("Проверить ответ удаления"):
        assert_status_code(delete_response, 204)
        assert_response_has_header(delete_response, "date")
