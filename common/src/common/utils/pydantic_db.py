"""Helpers for persisting Pydantic models when some ORM columns are JSON."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date, datetime
from typing import Any
from uuid import UUID

# Fields on the order row whose *values* are stored as JSON (nested UUID/datetime
# must be stringified), while other columns keep native types for the DB driver.
json_fields: frozenset[str] = frozenset({"products"})


def _nested_json_compatible(obj: Any) -> Any:
    """
    Coerce a nested structure to JSON-encodable scalars and dicts (for JSONB).

    Top-level :class:`uuid.UUID` and :class:`~datetime.datetime` are left to
    normal ``model_dump()`` so TIMESTAMPTZ/UUID columns still receive real types.
    """
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json")
    if isinstance(obj, Mapping):
        return {k: _nested_json_compatible(v) for k, v in obj.items()}
    if isinstance(obj, Sequence) and not isinstance(obj, (str, bytes, bytearray)):
        return [_nested_json_compatible(x) for x in obj]
    return obj


def model_dump_for_orm(
    obj: Any,
    *,
    exclude_unset: bool,
    json_fields: frozenset[str],
) -> dict[str, Any]:
    """
    Build a dict for ``Model(**data)`` with native DB types, plus JSON fields fixed.

    :param obj: A Pydantic v2 model (or v1 with ``.dict``), or a mapping.
    :param exclude_unset: Use for partial updates.
    :param json_fields: ORM attribute names that map to a JSON/JSONB column
        and must not leave raw :class:`uuid.UUID` or datetimes in nested data.
    """
    if hasattr(obj, "model_dump"):
        data = obj.model_dump(exclude_unset=exclude_unset)
    elif hasattr(obj, "dict"):
        data = obj.dict(exclude_unset=exclude_unset)
    else:
        data = dict(obj)

    for fname in json_fields:
        if fname not in data:
            continue
        data[fname] = _nested_json_compatible(data[fname])
    return data
