from pydantic import BaseModel, ConfigDict, Field


class AdditionRequest(BaseModel):
    additional_info: str | None = None
    additional_number: int | None = None


class EntityRequest(BaseModel):
    title: str
    verified: bool
    addition: AdditionRequest | None = None
    important_numbers: list[int] = Field(default_factory=list)


class AdditionResponse(BaseModel):
    id: int | None = None
    additional_info: str | None = None
    additional_number: int | None = None


class EntityResponse(BaseModel):
    id: int
    title: str
    verified: bool
    addition: AdditionResponse | None = None
    important_numbers: list[int] = Field(default_factory=list)


class EntityFilterResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    entity: list[EntityResponse]
    page: int | None = None
    per_page: int | None = Field(default=None, alias="perPage")
