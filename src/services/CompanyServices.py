from fastapi import Depends, HTTPException, status, UploadFile
from uuid import uuid4
from Classes.PathExtend import PathExtend
from aiofiles import open
import os

from ..models.Company import *
from ..repositories.CompanyRepository import CompanyRepository
from ..repositories.UserRepository import UserRepository
from ..tables import Organizations


class CompanyServices:
    def __init__(self,
                 company_repository: CompanyRepository = Depends(),
                 user_repository: UserRepository = Depends()):
        self.__company_repository: CompanyRepository = company_repository
        self.__user_repo: UserRepository = user_repository
        self.__count_item: int = 20

    @property
    def count_item(self) -> int:
        return self.__count_item

    async def get_count_page_by_user(self, uuid_user: str) -> int:
        count_row = await self.__company_repository.count_row_by_user(uuid_user)
        i = int(count_row % self.__count_item != 0)
        return count_row // self.__count_item + i

    async def get_activiti(self) -> list[Activity]:
        response = await self.__company_repository.get_activiti()
        return [Activity.model_validate(i, from_attributes=True) for i in response]

    async def get_type_org(self) -> list[TypeOrganizations]:
        response = await self.__company_repository.get_type_organization()
        return [TypeOrganizations.model_validate(i, from_attributes=True) for i in response]

    async def get_list_company(self, num_page: int, uuid_user: str) -> list[GetCompany]:
        offset = (num_page - 1) * self.__count_item
        company_entity = await self.__company_repository.get_list_company_by_user(offset, self.__count_item, uuid_user)
        company_models = [GetCompany.model_validate(entity, from_attributes=True) for entity in company_entity]
        return company_models

    async def get_company(self, uuid_company: str) -> GetCompanyAndImg:
        entity = await self.__company_repository.get_by_uuid(uuid_company)
        return GetCompanyAndImg.model_validate(entity, from_attributes=True)

    async def add_company(self, company_data: PostCompany, icon: UploadFile, uuid_user: str):

        user = await self.__user_repo.get_by_uuid(uuid_user)

        file_path = ""
        if icon:
            file_path = await self.upload_file(icon)

        entity = Organizations(
            uuid=uuid4(),
            name=company_data.name,
            ogrn=company_data.ogrn,
            inn=company_data.inn,
            kpp=company_data.kpp,
            id_type_organizations=company_data.id_type_organizations,
            date_registration=company_data.date_registration,
            address=company_data.address,
            id_main_activity=company_data.id_main_activity,
            supervisor=company_data.supervisor,
            icon=file_path,
            id_user=user.id
        )

        await self.__company_repository.add(entity)

    async def upload_file(self, file: UploadFile) -> str:
        name, extend = file.filename.split(".")

        new_name = PathExtend.create_file_name(extension=extend)

        filepath = PathExtend(new_name)
        async with open(str(filepath), 'wb') as out_file:
            while content := await file.read(1024):
                await out_file.write(content)
        return str(filepath.path.name)

    async def update_company(self, company_data: PostCompany, icon: UploadFile, uuid_company: str):
        company = await self.__company_repository.get_by_uuid(uuid_company)

        file_path = ""
        if icon:
            os.remove(str(PathExtend(company.icon)))
            file_path = await self.upload_file(icon)

        company.name = company_data.name
        company.ogrn = company_data.ogrn
        company.inn = company_data.inn
        company.kpp = company_data.kpp
        company.date_registration = company_data.date_registration
        company.address = company_data.address
        company.id_main_activity = company_data.id_main_activity
        company.supervisor = company_data.supervisor
        if file_path != "":
            company.icon = file_path

        await self.__company_repository.update(company)

    async def delete_company(self, uuid_company: str):
        company = await self.__company_repository.get_by_uuid(uuid_company)
        if company.icon:
            os.remove(str(PathExtend(company.icon)))
        await self.__company_repository.delete(company)
