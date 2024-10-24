"""Module for handling command routes in the Redis application."""

from typing import Any, Annotated
from fastapi import APIRouter, Form
from redis_app.functions.cmd import (
    check_cache,
    get_value,
    add_entry,
    remove_entry,
    update_entry,
    get_entries,
    get_keys,
)
from redis_app.models.redis_handler import Config

router = APIRouter(prefix="/cmd", tags=["cmd"])


@router.get("/check_cache")
async def check_cache_endpoint(value: Any):
    """Endpoint to check if a value is in the cache."""
    return check_cache(value)


@router.get("/get_value")
async def get_value_endpoint(key: str):
    """Endpoint to get a value by its key."""
    return get_value(key)


@router.post("/add_entry")
async def add_entry_endpoint(key: Any, value: Any, config: Annotated[Config, Form()]):
    """Endpoint to add a new entry to the storage."""
    return add_entry(key, value, config)


@router.delete("/remove_entry")
async def remove_entry_endpoint(key: str):
    """Endpoint to remove an entry by its key."""
    return remove_entry(key)


@router.put("/update_entry")
async def update_entry_endpoint(key: str, value: Any):
    """Endpoint to update an existing entry."""
    return update_entry(key, value)


@router.get("/get_entries")
async def get_entries_endpoint():
    """Endpoint to retrieve all entries."""
    return get_entries()


@router.get("/get_keys")
async def get_keys_endpoint():
    """Endpoint to retrieve all keys."""
    return get_keys()
