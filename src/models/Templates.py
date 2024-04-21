from pydantic import BaseModel, UUID4, field_serializer


class Tag(BaseModel):
    id: int
    id_subtag: int | None = None
    name: str
    description: str


class TemplateUUID(BaseModel):
    uuid: UUID4

    @field_serializer('uuid')
    def serialize_dt(self, dt: UUID4, _info):
        return str(dt)


class BaseTemplate(BaseModel):
    name: str
    docs: str


class GetTemplateCreate(BaseTemplate, TemplateUUID):
    additional_fields: list | None
    tag: Tag


class GetTemplateUpdate(BaseTemplate, TemplateUUID):
    additional_fields: str | None
    tag: Tag


class PostTemplate(BaseTemplate):
    additional_fields: str | None
    id_tag: int


class GetTemplateView(TemplateUUID):
    name: str
    tag: Tag


class QueueTemplate(TemplateUUID):
    additional_fields: list | None


class CreateZipTemplate(BaseModel):
    queue_template: list[QueueTemplate]
    uuid_company: str
