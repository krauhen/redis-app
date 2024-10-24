"""
Module for handling Redis cache operations.

This module provides functions to check, get, add, remove, and update
entries in the Redis cache as well as retrieve all entries and keys.
"""

from typing import Any

from redis_app.models.redis_handler import Config
from redis_app.utils.redis_handler import RedisHandler

redis_handler = RedisHandler()


def check_cache(value: Any):
    """
    Check if a value is present in the Redis cache.

    Args:
        value (Any): The value to check in the cache.

    Returns:
        bool: True if the value is found in the cache, False otherwise.
    """
    return redis_handler.check_cache(value)


def get_value(key: str):
    """
    Retrieve a value from the Redis cache by its key.

    Args:
        key (str): The key for the value in the cache.

    Returns:
        Any: The value associated with the key or None if not found.
    """
    return redis_handler.get_value_by_hash(key)


def add_entry(key: Any, value: Any, config: Config | None):
    """
    Add a new entry to the Redis cache.

    Args:
        key (Any): The key for the entry.
        value (Any): The value to be stored.
        config (Config | None): Optional configuration for the entry.

    Returns:
        bool: True if the entry was added successfully, False otherwise.
    """
    return redis_handler.add_entry(key, value, config)


def remove_entry(key: str):
    """
    Remove an entry from the Redis cache by its key.

    Args:
        key (str): The key for the entry to be removed.

    Returns:
        bool: True if the entry was removed successfully, False otherwise.
    """
    return redis_handler.remove_entry_by_hash(key)


def update_entry(key: str, value: Any):
    """
    Update an existing entry in the Redis cache.

    Args:
        key (str): The key for the entry to be updated.
        value (Any): The new value to be stored.

    Returns:
        bool: True if the entry was updated successfully, False otherwise.
    """
    return redis_handler.update_entry_by_hash(key, value)


def get_entries():
    """
    Retrieve all entries from the Redis cache.

    Returns:
        list: A list of all entries in the cache.
    """
    return redis_handler.get_entries()


def get_keys():
    """
    Retrieve all keys from the Redis cache.

    Returns:
        list: A list of all keys in the cache.
    """
    return redis_handler.get_key_hashes()
