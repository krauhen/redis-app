from typing import Any

from redis_app.models.redis_handler import Config
from redis_app.utils.redis_handler import RedisHandler

redis_handler = RedisHandler()


def check_cache(value: Any):
    return redis_handler.check_cache(value)


def get_value(key: str):
    return redis_handler.get_value_by_hash(key)


def add_entry(key: Any, value: Any, config: Config | None):
    return redis_handler.add_entry(key, value, config)


def remove_entry(key: str):
    return redis_handler.remove_entry_by_hash(key)


def update_entry(key: str, value: Any):
    return redis_handler.update_entry_by_hash(key, value)


def get_entries():
    return redis_handler.get_entries()


def get_keys():
    return redis_handler.get_key_hashes()
