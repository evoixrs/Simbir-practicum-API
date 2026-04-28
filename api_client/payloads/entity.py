from uuid import uuid4

from api_client.models.entity import AdditionRequest, EntityRequest


def create_entity_payload() -> EntityRequest:
    unique_suffix = uuid4().hex[:8]
    return EntityRequest(
        title=f"Заголовок сущности {unique_suffix}",
        verified=True,
        addition=AdditionRequest(
            additional_info=f"Дополнительные сведения {unique_suffix}",
            additional_number=123,
        ),
        important_numbers=[42, 87, 15],
    )


def create_second_entity_payload() -> EntityRequest:
    unique_suffix = uuid4().hex[:8]
    return EntityRequest(
        title=f"Заголовок сущности 2 {unique_suffix}",
        verified=True,
        addition=AdditionRequest(
            additional_info=f"Дополнительные сведения 2 {unique_suffix}",
            additional_number=456,
        ),
        important_numbers=[10, 20, 30],
    )


def patch_entity_payload() -> EntityRequest:
    unique_suffix = uuid4().hex[:8]
    return EntityRequest(
        title=f"Обновленный заголовок сущности {unique_suffix}",
        verified=False,
        addition=AdditionRequest(
            additional_info=f"Обновленные дополнительные сведения {unique_suffix}",
            additional_number=456,
        ),
        important_numbers=[10, 20, 30],
    )
