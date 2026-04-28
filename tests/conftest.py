import logging
import os
from collections.abc import Generator
from dataclasses import dataclass
from http import HTTPStatus

import pytest
from dotenv import load_dotenv

from api_client.client import EntityClient
from api_client.models.entity import EntityRequest, EntityResponse
from api_client.payloads.entity import create_entity_payload, create_second_entity_payload
from helpers.assert_helpers import assert_status_code
from helpers.response_helpers import deserialize_entity, get_created_entity_id


logger = logging.getLogger("api_tests")
load_dotenv()


@dataclass
class CreatedEntity:
    entity_id: int
    payload: EntityRequest
    entity: EntityResponse
    is_deleted: bool = False


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--base-url",
        action="store",
        default=None,
        help="Base URL of API test stand",
    )


@pytest.fixture(scope="session")
def base_url(request: pytest.FixtureRequest) -> str:
    url = request.config.getoption("--base-url") or os.getenv("BASE_URL")
    if not url:
        pytest.fail("Set API base URL with --base-url or BASE_URL in .env")

    logger.info("Base API URL: %s", url)
    return url


@pytest.fixture(scope="session")
def api_client(base_url: str) -> EntityClient:
    return EntityClient(base_url=base_url)


def create_test_entity(
    api_client: EntityClient,
    payload: EntityRequest,
) -> CreatedEntity:
    create_response = api_client.create_entity(
        payload=payload.model_dump(exclude_none=True),
    )
    assert_status_code(create_response, HTTPStatus.OK)
    entity_id = get_created_entity_id(create_response)

    get_response = api_client.get_entity(entity_id=entity_id)
    assert_status_code(get_response, HTTPStatus.OK)
    entity = deserialize_entity(get_response)

    return CreatedEntity(
        entity_id=entity_id,
        payload=payload,
        entity=entity,
    )


@pytest.fixture
def created_entity(api_client: EntityClient) -> Generator[CreatedEntity, None, None]:
    entity = create_test_entity(
        api_client=api_client,
        payload=create_entity_payload(),
    )

    try:
        yield entity
    finally:
        # DELETE-тест удаляет сущность сам, поэтому cleanup пропускает повторное удаление.
        if entity.is_deleted:
            return

        delete_response = api_client.delete_entity(entity_id=entity.entity_id)
        if delete_response.status_code != HTTPStatus.NO_CONTENT:
            logger.warning(
                "Failed to delete test entity %s. Status: %s. Body: %s",
                entity.entity_id,
                delete_response.status_code,
                delete_response.text,
            )


@pytest.fixture
def created_entities(
    api_client: EntityClient,
) -> Generator[list[CreatedEntity], None, None]:
    entities = [
        create_test_entity(
            api_client=api_client,
            payload=create_entity_payload(),
        ),
        create_test_entity(
            api_client=api_client,
            payload=create_second_entity_payload(),
        ),
    ]

    try:
        yield entities
    finally:
        for entity in entities:
            # DELETE-тест удаляет сущность сам, поэтому cleanup пропускает повторное удаление.
            if entity.is_deleted:
                continue

            delete_response = api_client.delete_entity(entity_id=entity.entity_id)
            if delete_response.status_code != HTTPStatus.NO_CONTENT:
                logger.warning(
                    "Failed to delete test entity %s. Status: %s. Body: %s",
                    entity.entity_id,
                    delete_response.status_code,
                    delete_response.text,
                )
