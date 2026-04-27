from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


class BaseRepository[ModelType: DeclarativeBase]:
    def __init__(self, session: AsyncSession, model: type[ModelType]) -> None:
        self.model = model
        self.session = session

    async def create(self, obj_in) -> ModelType:
        if hasattr(obj_in, "model_dump"):
            obj_data = obj_in.model_dump()
        elif hasattr(obj_in, "dict"):
            obj_data = obj_in.dict()
        else:
            obj_data = dict(obj_in)

        db_obj = self.model(**obj_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: ModelType, obj_in) -> ModelType:
        if hasattr(obj_in, "model_dump"):
            obj_data = obj_in.model_dump(exclude_unset=True)
        elif hasattr(obj_in, "dict"):
            obj_data = obj_in.dict(exclude_unset=True)
        else:
            obj_data = dict(obj_in)

        for field, value in obj_data.items():
            setattr(db_obj, field, value)

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, obg_id: UUID) -> bool:
        obj = await self.get(obg_id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
            return True
        return False

    async def get(self, obg_id: UUID) -> ModelType | None:
        return await self.session.get(self.model, obg_id)

    async def get_all(self) -> list[ModelType]:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def filter_by(self, **kwargs) -> list[ModelType]:
        stmt = select(self.model)
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                stmt = stmt.where(getattr(self.model, key) == value)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())
