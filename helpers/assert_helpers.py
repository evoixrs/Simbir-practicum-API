from requests import Response

from api_client.models.entity import EntityRequest, EntityResponse


def assert_status_code(response: Response, expected_status_code: int) -> None:
    assert response.status_code == expected_status_code, (
        f"Expected status code {expected_status_code}, "
        f"got {response.status_code}. Response body: {response.text}"
    )


def assert_content_type(response: Response, expected_content_type: str) -> None:
    actual_content_type = response.headers.get("content-type") or ""
    assert expected_content_type in actual_content_type, (
        f"Expected content-type to contain '{expected_content_type}', "
        f"got '{actual_content_type}'"
    )


def assert_response_has_header(response: Response, header_name: str) -> None:
    assert header_name in response.headers, (
        f"Expected response header '{header_name}'. "
        f"Actual headers: {dict(response.headers)}"
    )


def assert_entity_matches_payload(
    entity: EntityResponse,
    payload: EntityRequest,
) -> None:
    assert entity.title == payload.title, (
        f"Expected title '{payload.title}', got '{entity.title}'"
    )
    assert entity.verified == payload.verified, (
        f"Expected verified '{payload.verified}', got '{entity.verified}'"
    )
    assert entity.important_numbers == payload.important_numbers, (
        f"Expected important_numbers '{payload.important_numbers}', "
        f"got '{entity.important_numbers}'"
    )

    if payload.addition is None:
        assert entity.addition is None, "Expected addition to be empty"
        return

    assert entity.addition is not None, "Expected addition in response"
    assert entity.addition.additional_info == payload.addition.additional_info, (
        f"Expected additional_info '{payload.addition.additional_info}', "
        f"got '{entity.addition.additional_info}'"
    )
    assert entity.addition.additional_number == payload.addition.additional_number, (
        f"Expected additional_number '{payload.addition.additional_number}', "
        f"got '{entity.addition.additional_number}'"
    )


def assert_entity_has_ids(entity: EntityResponse) -> None:
    assert entity.id > 0, f"Expected entity id to be positive, got '{entity.id}'"
    assert entity.addition is not None, "Expected addition in response"
    assert entity.addition.id is not None, "Expected addition id in response"
    assert entity.addition.id > 0, (
        f"Expected addition id to be positive, got '{entity.addition.id}'"
    )


def assert_entities_contain_ids(
    entities: list[EntityResponse],
    expected_ids: list[int],
) -> None:
    actual_ids = [entity.id for entity in entities]
    for expected_id in expected_ids:
        assert expected_id in actual_ids, (
            f"Expected entity id '{expected_id}' in list. Actual ids: {actual_ids}"
        )
