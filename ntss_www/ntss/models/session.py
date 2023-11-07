"""
This handles session management
"""
import json
import atexit
from uuid import uuid4
import time
from datetime import datetime, timedelta
from redis import Redis


class RedisSession:
    """
    Redis Session Manager
    """
    
    def __init__(self, expiration: int = 7200):
        """
        Initializes the Redis cache
        """
        self.cache = Redis(host='redis_cache', port=6379, db=0, decode_responses=True)
        self._expiration = expiration
        atexit.register(self._cleanup)

    def _cleanup(self):
        """
        Cleans up the cache
        """
        self.cache.quit()

    def add_to_cache(self, key: str, val: any) -> bool:
        """
        Adds a value to the cache
        """
        if self.cache.set(key, val, ex=self._expiration):
            return True
        return False

    def append_to_cache_key(self, key: str, val: any) -> bool:
        """
        Appends a value to a cache key
        """
        if self.cache.append(key, val):
            return True
        return False

    def get_from_cache(self, key, serialized=False) -> str | dict | list:
        """
        Returns a key from the cache
        """
        if serialized:
            cache_val = self.cache.dump(key)
        else:
            cache_val = self.cache.get(key)
        return cache_val

    def does_key_exist(self, key: str) -> bool:
        """
        Checks if a key exists in Redis
        """
        if self.cache.exists(key) > 0:
            return True
        return False

    def remove_key(self, key: str | list) -> bool:
        """
        Removes a key from redis
        """
        if isinstance(key, str) and self.does_key_exist(key):
            if self.cache.delete(key) == 1:
                return True
            return False
        return self._remove_keys(key)

    def _remove_keys(self, keys) -> bool:
        """
        Remove the listed keys from Redis
        """
        deleted = False
        for cache_key in keys:
            if self.does_key_exist(cache_key) and self.cache.delete(keys) == 1:
                deleted = True
        return deleted

    def set_key_expiration(self, key, expiration: int = 7200):
        """
        Set the expiration time of a key in Redis
        """
        return self.cache.expire(key, expiration)

    def get_key_expiration(self, key: str, get_datetime: bool = False) -> int | datetime:
        """
        Get the expiration time of a key in Redis
        """
        seconds = self.cache.ttl(key)
        # convert seconds to unixtimestamp
        unixtime = int(time.time()) + seconds
        if get_datetime:
            return datetime.utcfromtimestamp(unixtime)
        return unixtime


class Session(RedisSession):
    """
    This class will do session management for users
    """
    _max_age = 7200
    _secure = True
    _httponly = True
    _samesite = 'strict'
    _path = '/'
    _session_id = ''
    _session_data = {}

    def add_session(self, session_data: dict) -> str:
        """
        Method to add session information
        """
        self._session_id = self._create_unique_id()
        self._session_data = session_data
        session_value = json.dumps(self._session_data)
        self.add_to_cache(self._session_id, session_value)
        return self._session_id

    def get_session_id(self):
        """
        Returns the session id
        """
        return self._session_id

    def get_session(self, session_id: str) -> dict:
        """
        Returns a dictionary of a session
        """
        self._session_data = {}
        if self.does_key_exist(session_id):
            self._session_data = json.loads(self.get_from_cache(session_id))
        return self._session_data

    def update_session(self, session_id: str, session_data: dict) -> None:
        """
        Makes updates to the session
        """
        self._session_data = session_data
        json_data = json.dumps(session_data)
        self.add_to_cache(session_id, json_data)

    def delete_session(self, session_id: str) -> None:
        """
        Remove the session if it's expired
        """
        self.remove_key(session_id)
        self._session_id = ''
        self._session_data = {}

    def renew_session(self, session_id: str) -> bool:
        """
        Renew a session if the id exists
        """
        if self.does_key_exist(session_id):
            self.set_key_expiration(session_id)
            return True
        return False

    def get_session_expiration(self, session_id: str) -> datetime:
        """
        Get the expiration time of the session
        """
        if not self.does_key_exist(session_id):
            return datetime().now() - timedelta(seconds=1)
        return self.get_key_expiration(session_id, True)

    def _create_unique_id(self):
        """
        Generates a unique session id
        """
        return uuid4().hex
