from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from ..tables import Organizations, TypeOrganizations, Activity, User
from ..database import get_session

from fastapi import Depends


class CompanyRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.__session: AsyncSession = session

    async def count_row_by_user(self, uuid_user: str) -> int:
        response = select(func.count(Organizations.id)).join(User).where(User.uuid == uuid_user)
        result = await self.__session.execute(response)
        return result.scalars().first()

    async def get_activiti(self) -> list[Activity]:
        response = select(Activity)
        result = await self.__session.execute(response)
        return result.scalars().all()

    async def get_type_organization(self) -> list[TypeOrganizations]:
        response = select(TypeOrganizations)
        result = await self.__session.execute(response)
        return result.scalars().all()

    async def get_list_company_by_user(self, start: int, limit: int, uuid_user: str) -> list[Organizations]:
        response = select(Organizations).join(User).where(User.uuid == uuid_user)
        response = response.offset(start).fetch(limit).order_by(Organizations.id)
        result = await self.__session.execute(response)
        return result.unique().scalars().all()

    async def add(self, company: Organizations) -> Organizations | None:
        try:
            self.__session.add(company)
            await self.__session.commit()
            return company
        except:
            await self.__session.rollback()
            return None

    async def update(self, company: Organizations):
        try:
            self.__session.add(company)
            await self.__session.commit()
        except:
            await self.__session.rollback()
            raise Exception

    async def delete(self, company: Organizations):
        try:
            await self.__session.delete(company)
            await self.__session.commit()
        except:
            await self.__session.rollback()
            raise Exception

    async def get_by_uuid(self, uuid_company: str) -> Organizations:
        query = select(Organizations).where(Organizations.uuid == uuid_company)
        result = await self.__session.execute(query)
        return result.scalars().first()

