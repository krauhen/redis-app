from fastapi import APIRouter
from typing import Annotated
from fastapi import Form
from redis_app.functions.cmd import *

router = APIRouter(prefix="/cmd", tags=["cmd"])


@router.get("/check_cache")
async def check_cache_endpoint(value: Any):
    return check_cache(value)


@router.get("/get_value")
async def get_value_endpoint(key: str):
    return get_value(key)


@router.post("/add_entry")
async def add_entry_endpoint(key: Any, value: Any, config: Annotated[Config, Form()]):
    return add_entry(key, value, config)


@router.delete("/remove_entry")
async def remove_entry_endpoint(key: str):
    return remove_entry(key)


@router.put("/update_entry")
async def update_entry_endpoint(key: str, value: Any):
    return update_entry(key, value)


@router.get("/get_entries")
async def get_entries_endpoint():
    return get_entries()


@router.get("/get_keys")
async def get_keys_endpoint():
    return get_keys()
