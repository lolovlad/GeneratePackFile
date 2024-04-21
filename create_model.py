from src.tables import User, TypeUser, Activity, Tag, TypeOrganizations
from src.database import async_session
from asyncio import run
from uuid import uuid4


async def create_tag_context():
    async with async_session() as session:
        type_task = [
            Tag(
                uuid=uuid4(),
                name="Общие документы",
                description="Общие документы"
            ),
            Tag(
                uuid=uuid4(),
                name="Комерческая тайна",
                description="Комерческая тайна"
            ),
            Tag(
                uuid=uuid4(),
                name="ПДн",
                description="ПДн"
            )
        ]

        session.add_all(type_task)
        await session.commit()

        type_task = [
            Tag(
                uuid=uuid4(),
                name="Политика ИБ",
                description="Политика ИБ",
                id_subtag=1
            ),
            Tag(
                uuid=uuid4(),
                name="Положение о КТ",
                description="Положение о КТ",
                id_subtag=2
            ),
            Tag(
                uuid=uuid4(),
                name="Положения и политики",
                description="Положения и политики",
                id_subtag=3
            )
        ]
        session.add_all(type_task)
        await session.commit()


async def create_activity_context():
    async with async_session() as session:
        activity = [
            Activity(
                name="Разработка компьютерного программного обеспечения",
                code="62.01",
                description=""
            ),
            Activity(
                name="Деятельность в области связи на базе проводных технологий",
                code="62.10",
                description=""
            )
        ]
        session.add_all(activity)
        await session.commit()


async def create_type_organization_context():
    async with async_session() as session:
        types = [
            TypeOrganizations(
                name="OOO",
                description="ООО"
            ),
            TypeOrganizations(
                name="PAO",
                description="ПАО"
            ),
            TypeOrganizations(
                name="IP",
                description="ИП"
            )
        ]
        session.add_all(types)
        await session.commit()


async def create_model():
    async with async_session() as session:
        types_user = [
            TypeUser(
                name="admin",
                description="admin"
            ),
            TypeUser(
                name="user",
                description="user"
            )
        ]

        user = User(
            email="admin@admin.com",
            id_type=1,
            name="Иван",
            surname="Иван",
            patronymic="Иван",
            phone="89053626466"
        )
        user.password = "admin"
        session.add_all(types_user)
        session.add(user)

        await session.commit()


async def main():
    await create_model()
    await create_tag_context()
    await create_activity_context()
    await create_type_organization_context()


run(main())