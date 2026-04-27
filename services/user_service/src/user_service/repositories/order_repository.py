from sqlalchemy.ext.asyncio import AsyncSession

from common.persistence import BaseRepository
from common.persistence.models import Order
from common.utils.pydantic_db import ORDER_NESTED_JSON_COLUMN_FIELDS, model_dump_for_orm


class OrdersRepository(BaseRepository[Order]):
    """Orders Repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Init Orders Repository."""

        super().__init__(session, Order)

    async def create(self, obj_in) -> Order:
        obj_data = model_dump_for_orm(
            obj_in,
            exclude_unset=False,
            json_fields=ORDER_NESTED_JSON_COLUMN_FIELDS,
        )
        db_obj = self.model(**obj_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: Order, obj_in) -> Order:
        obj_data = model_dump_for_orm(
            obj_in,
            exclude_unset=True,
            json_fields=ORDER_NESTED_JSON_COLUMN_FIELDS,
        )
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj
