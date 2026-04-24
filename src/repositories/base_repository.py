from typing import TypeVar, Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseRepository:
    """
    Base repository class providing basic CRUD operations for database models.

    :param model: SQLAlchemy model class
    :param session: Async database session
    """

    def __init__(self, session: AsyncSession, model: Type[ModelType]) -> None:
        """
        Initialize repository with model and session.

        :param model: SQLAlchemy model class
        :param session: Async database session
        """
        self.model = model
        self.session = session

    async def create(self, obj_in) -> ModelType:
        """
        Create a new record in database.

        :param obj_in: Pydantic schema or dict with creation data
        :returns: Created model instance
        """
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
        """
        Update an existing record.

        :param db_obj: Database model instance to update
        :param obj_in: Pydantic schema or dict with update data
        :returns: Updated model instance
        """
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

    async def delete(self, obg_id: int) -> bool:
        """
        Delete a record by ID.

        :param obg_id: Record identifier
        :returns: True if deleted, False if not found
        """
        obj = await self.get(obg_id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
            return True
        return False

    async def get(self, obg_id: int) -> ModelType | None:
        """
        Get a record by ID.

        :param obg_id: Record identifier
        :returns: Model instance or None if not found
        """
        return await self.session.get(self.model, obg_id)

    async def get_all(self) -> list[ModelType]:
        """
        Get all records from database.

        :returns: List of model instances
        """
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
