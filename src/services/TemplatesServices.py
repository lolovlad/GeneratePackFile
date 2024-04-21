from fastapi import Depends, HTTPException, status, UploadFile
from uuid import uuid4
from Classes.PathExtend import PathExtend
from aiofiles import open as open_aio
import os

from ..models.Templates import *
from ..models.Company import GetCompany
from ..repositories.TemplatesRepository import TemplatesRepository
from ..repositories.CompanyRepository import CompanyRepository
from ..tables import FileTemplate, Organizations
from json import load

from docxtpl import DocxTemplate, InlineImage
import io
import zipfile
from docx.shared import Mm
from pathlib import Path


class TemplatesServices:
    def __init__(self,
                 template_repository: TemplatesRepository = Depends(),
                 company_repository: CompanyRepository = Depends()
                 ):
        self.__template_repository: TemplatesRepository = template_repository
        self.__company_repository: CompanyRepository = company_repository
        self.__count_item: int = 20

    @property
    def count_item(self) -> int:
        return self.__count_item

    async def get_count_page(self) -> int:
        count_row = await self.__template_repository.count_row()
        i = int(count_row % self.__count_item != 0)
        return count_row // self.__count_item + i

    async def get_tags_children(self, id_tag: int) -> list[Tag]:
        response = await self.__template_repository.get_tags_children(id_tag)
        return [Tag.model_validate(i, from_attributes=True) for i in response]

    async def get_tags_parent(self) -> list[Tag]:
        response = await self.__template_repository.get_tags_parent()
        return [Tag.model_validate(i, from_attributes=True) for i in response]

    async def get_list_templates(self, num_page: int) -> list[GetTemplateUpdate]:
        offset = (num_page - 1) * self.__count_item
        templates_entity = await self.__template_repository.get_list_files(offset, self.__count_item)
        templates_models = [GetTemplateUpdate.model_validate(entity, from_attributes=True) for entity in templates_entity]
        return templates_models

    async def get_template_update(self, uuid_company: str) -> GetTemplateUpdate:
        entity = await self.__template_repository.get_by_uuid(uuid_company)
        return GetTemplateUpdate.model_validate(entity, from_attributes=True)

    async def get_template_create(self, uuid_company: str) -> GetTemplateCreate:
        template = await self.__template_repository.get_by_uuid(uuid_company)

        json_fields = None

        if template.additional_fields is not None:
            with open(str(PathExtend(template.additional_fields)), 'r') as out_file:
                json_fields = load(out_file)
            template.additional_fields = json_fields

        return GetTemplateCreate.model_validate(template, from_attributes=True)

    async def add(self, name: str, docs: UploadFile, additional_fields: UploadFile | None, id_tag: int):
        docs_path = await self.upload_file(docs)
        json_path = None
        if additional_fields:
            json_path = await self.upload_file(additional_fields)

        entity = FileTemplate(
            uuid=uuid4(),
            name=name,
            docs=docs_path,
            additional_fields=json_path,
            id_tag=id_tag
        )

        await self.__template_repository.add(entity)

    async def upload_file(self, file: UploadFile) -> str:
        name, extend = file.filename.split(".")

        new_name = PathExtend.create_file_name(extension=extend)

        filepath = PathExtend(new_name)
        async with open_aio(str(filepath), 'wb') as out_file:
            while content := await file.read(1024):
                await out_file.write(content)
        return str(filepath.path.name)

    async def update(self, uuid_template: str, name: str, docs: UploadFile | None, additional_fields: UploadFile | None, id_tag: int):
        template = await self.__template_repository.get_by_uuid(uuid_template)

        docs_path = None
        json_path = None
        if docs:
            os.remove(str(PathExtend(template.docs)))
            docs_path = await self.upload_file(docs)

        if additional_fields:
            os.remove(str(PathExtend(template.additional_fields)))
            json_path = await self.upload_file(additional_fields)


        template.name = name
        template.id_tag = id_tag

        if docs_path is not None:
            template.docs = docs_path

        if docs_path is not None:
            template.additional_fields = json_path

        await self.__template_repository.update(template)

    async def delete(self, uuid_template: str):
        template = await self.__template_repository.get_by_uuid(uuid_template)
        if template.docs:
            os.remove(str(PathExtend(template.docs)))

        if template.additional_fields:
            os.remove(str(PathExtend(template.additional_fields)))
        await self.__template_repository.delete(template)

    async def get_list_template_by_tag_id(self, id_tag: int) -> list[GetTemplateView]:
        template = await self.__template_repository.get_list_by_id_tag(id_tag)
        return [GetTemplateView.model_validate(i, from_attributes=True) for i in template]

    async def create_pack_doc(self, queue_template: list[QueueTemplate], uuid_company: str):
        company = await self.__company_repository.get_by_uuid(uuid_company)
        zip_file = io.BytesIO()

        company_context = self.create_context_company(company)

        is_icon = len(company.icon) > 0

        with zipfile.ZipFile(zip_file, mode='w') as z:

            for item in queue_template:
                template = await self.__template_repository.get_by_uuid(item.uuid)

                prefab = DocxTemplate(str(PathExtend(template.docs)))
                template_file = io.BytesIO()

                if is_icon:
                    company_context["icon"] = InlineImage(prefab, str(PathExtend(company.icon)), width=Mm(30), height=Mm(12))


                context = {
                    "org": company_context,
                    "var": self.create_context_field(item.additional_fields)
                }

                prefab.render(context)
                prefab.save(template_file)
                template_file.seek(0)
                name, ext = Path(template.docs).name.split(".")
                z.writestr(f"{template.name}.{ext}", template_file.read())
        zip_file.seek(0)
        return zip_file

    def create_context_company(self, company: Organizations) -> dict:
        org = GetCompany.model_validate(company, from_attributes=True)
        org_dict = org.model_dump()
        if company.type_organizations.name == "OOO":
            org_dict["full_type_name"] = "Общество с ограниченой ответсвенностью"
        elif company.type_organizations.name == "PAO":
            org_dict["full_type_name"] = "Публичное акционерное общество"
        else:
            org_dict["full_type_name"] = "Индивидуальный предприниматель"
        return org_dict

    def create_context_field(self, fields: list | None) -> dict:
        field_dict = {}
        if fields is None:
            return field_dict
        for field in fields:
            field_dict[field["name"]] = field["val"]
        return field_dict