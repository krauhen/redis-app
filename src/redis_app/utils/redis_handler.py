import hashlib
import json
import base64
import redis

from typing import Any, Dict, List, Tuple, Set

from redis_app.models.redis_handler import Config


def _hash(key):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(key.encode('utf-8'))
    hash_key = sha256_hash.hexdigest()
    return hash_key


def stringify(value: Any) -> str:
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
                result = base64.b64encode(value).decode('utf-8')
            except UnicodeDecodeError:
                result = base64.b64encode(value.decode('latin-1').encode()).decode('utf-8')
        else:
            result = json.dumps(value)
    except Exception as _:
        result = "null"

    return result


class RedisHandler:
    def __init__(self):
        super().__init__()
        self._redis = redis.Redis(host='redis', port=6379, db=0)

    def check_cache(self, key: Any):
        key_str = stringify(key)
        key_hash = _hash(key_str)
        response = self._redis.get(key_hash)
        hit = response is not None
        value = response if response is not None else None
        return hit, value

    def get_value_by_hash(self, key_hash: str):
        return self._redis.get(key_hash)

    def add_entry(self, key: Any, value: Any, config: Config | None):
        key_str = stringify(key)
        key_hash = _hash(key_str)
        self._redis.set(key_hash, value, **config.dict())
        return key_hash

    def remove_entry_by_hash(self, key: Any):
        key_str = stringify(key)
        key_hash = _hash(key_str)
        self._redis.delete(key_hash)

    def update_entry_by_hash(self, key_hash: str, value: Any):
        self._redis.delete(key_hash)
        self._redis.set(key_hash, value)

    def get_entries(self):
        key_hashes = self._redis.keys()
        entries = [(key_hash, self._redis.get(key_hash)) for key_hash in key_hashes]
        return entries

    def get_key_hashes(self):
        return self._redis.keys()
