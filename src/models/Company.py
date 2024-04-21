from typing import List
from enum import Enum
from pydantic import BaseModel, UUID4, field_serializer

from datetime import datetime


class TypeOrganizations(BaseModel):
    id: int
    name: str
    description: str


class Activity(BaseModel):
    id: int
    name: str
    code: str
    description: str


class CompanyUUID(BaseModel):
    uuid: UUID4

    @field_serializer('uuid')
    def serialize_dt(self, dt: UUID4, _info):
        return str(dt)


class BaseCompany(BaseModel):
    name: str
    ogrn: str
    inn: str
    kpp: str
    address: str
    supervisor: str | None


class GetCompany(BaseCompany, CompanyUUID):
    date_registration: datetime
    type_organizations: TypeOrganizations
    main_activity: Activity


class PostCompany(BaseCompany):
    id_type_organizations: int
    id_main_activity: int | None
    date_registration: datetime


class GetCompanyAndImg(GetCompany):
    icon: str | None


class UpdateCompany(BaseCompany, CompanyUUID):
    id_main_activity: int
    date_registration: datetime