"""
This module provides utility functions for interacting with Redis,
including hashing keys and serializing data for storage in a Redis database.
"""

import hashlib
import json
import base64

from typing import Any, Dict, List, Tuple, Set

import redis

from redis_app.models.redis_handler import Config


def _hash(key: str) -> str:
    """
    Generate a SHA-256 hash of the given key.

    :param key: The key to be hashed.
    :return: The hashed key as a hexadecimal string.
    """
    sha256_hash = hashlib.sha256()
    sha256_hash.update(key.encode("utf-8"))
    hash_key = sha256_hash.hexdigest()
    return hash_key


def stringify(value: Any) -> str:
    """
    Convert a value to a JSON string representation.

    Handles various types including strings, dictionaries, lists, tuples,
    sets, numbers, booleans, and bytes.

    :param value: The value to be stringified.
    :return: A JSON string representation of the value.
    """
    try:
        if isinstance(value, str):
            result = value
        elif isinstance(value, Dict):
            result = json.dumps(value)
        elif isinstance(value, List):
            result = json.dumps(value)
        elif isinstance(value, Tuple):
            result = json.dumps(value)
        elif isinstance(value, Set):
            result = json.dumps(list(value))
        elif isinstance(value, (int, float)):
            result = str(value)
        elif isinstance(value, bool):
            result = str(value)
        elif isinstance(value, bytes):
            try:
                result = base64.b64encode(value).decode("utf-8")
            except (UnicodeDecodeError, AttributeError):
                result = base64.b64encode(value.decode("latin-1").encode()).decode(
                    "utf-8"
                )
        else:
            result = json.dumps(value)
    except (TypeError, ValueError):
        result = "null"

    return result


class RedisHandler:
    """
    A handler for interacting with a Redis database.
    """

    def __init__(self, host="redis", port=6379, db=0):
        """
        Initialize the RedisHandler and connect to the Redis database.
        """
        super().__init__()
        self._redis = redis.Redis(host=host, port=port, db=db)

    def check_cache(self, key: Any) -> Tuple[bool, Any]:
        """
        Check if a key exists in the cache.

        :param key: The key to check in the cache.
        :return: A tuple containing a boolean indicating if the key exists
                 and the value associated with the key, or None if it does not exist.
        """
        key_str = stringify(key)
        key_hash = _hash(key_str)
        response = self._redis.get(key_hash)
        hit = response is not None
        value = response if response is not None else None
        return hit, value

    def get_value_by_hash(self, key_hash: str) -> Any:
        """
        Retrieve a value from Redis by its hash.

        :param key_hash: The hash of the key to retrieve.
        :return: The value associated with the key hash, or None if not found.
        """
        return self._redis.get(key_hash)

    def add_entry(self, key: Any, value: Any, config: Config | None) -> str:
        """
        Add an entry to the Redis database under the given key.

        :param key: The key under which to store the value.
        :param value: The value to store.
        :param config: Additional configuration for setting the value.
        :return: The hash of the stored key.
        """
        key_str = stringify(key)
        key_hash = _hash(key_str)
        self._redis.set(key_hash, value, **config.dict())
        return key_hash

    def remove_entry_by_hash(self, key: Any) -> None:
        """
        Remove an entry from Redis by its key.

        :param key: The key to remove from the Redis database.
        """
        key_str = stringify(key)
        key_hash = _hash(key_str)
        self._redis.delete(key_hash)

    def update_entry_by_hash(self, key_hash: str, value: Any) -> None:
        """
        Update an entry in Redis by overwriting the value for a given key hash.

        :param key_hash: The hash of the key to update.
        :param value: The new value to set for the key.
        """
        self._redis.delete(key_hash)
        self._redis.set(key_hash, value)

    def get_entries(self) -> List[Tuple[str, Any]]:
        """
        Retrieve all entries from the Redis store.

        :return: A list of tuples containing key hashes and their associated values.
        """
        key_hashes = self._redis.keys()
        entries = [(key_hash, self._redis.get(key_hash)) for key_hash in key_hashes]
        return entries

    def get_key_hashes(self) -> List[str]:
        """
        Get all key hashes currently stored in the Redis database.

        :return: A list of key hashes.
        """
        return self._redis.keys()
