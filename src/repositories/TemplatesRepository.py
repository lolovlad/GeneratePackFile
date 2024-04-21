from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from ..tables import Tag, FileTemplate
from ..database import get_session

from fastapi import Depends


class TemplatesRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.__session: AsyncSession = session

    async def count_row(self) -> int:
        response = select(func.count(FileTemplate.id))
        result = await self.__session.execute(response)
        return result.scalars().first()

    async def get_tags_children(self, id_tag: int) -> list[Tag]:
        response = select(Tag).where(Tag.id_subtag == id_tag)
        result = await self.__session.execute(response)
        return result.unique().scalars().all()

    async def get_tags_parent(self):
        response = select(Tag).where(Tag.id_subtag == None)
        result = await self.__session.execute(response)
        return result.unique().scalars().all()

    async def get_list_files(self, start: int, limit: int) -> list[FileTemplate]:
        response = select(FileTemplate)
        response = response.offset(start).fetch(limit).order_by(FileTemplate.id)
        result = await self.__session.execute(response)
        return result.unique().scalars().all()

    async def add(self, temp: FileTemplate) -> FileTemplate | None:
        try:
            self.__session.add(temp)
            await self.__session.commit()
            return temp
        except:
            await self.__session.rollback()
            return None

    async def update(self, temp: FileTemplate):
        try:
            self.__session.add(temp)
            await self.__session.commit()
        except:
            await self.__session.rollback()
            raise Exception

    async def delete(self, temp: FileTemplate):
        try:
            await self.__session.delete(temp)
            await self.__session.commit()
        except:
            await self.__session.rollback()
            raise Exception

    async def get_by_uuid(self, uuid_template: str) -> FileTemplate:
        query = select(FileTemplate).where(FileTemplate.uuid == uuid_template)
        result = await self.__session.execute(query)
        return result.scalars().first()

    async def get_list_by_id_tag(self, id_tag: int) -> list[FileTemplate]:
        query = select(FileTemplate).where(FileTemplate.id_tag == id_tag)
        result = await self.__session.execute(query)
        return result.scalars().all()
