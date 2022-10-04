import hashlib
from diskcache import Cache
from functools import wraps

def cache_wrapper(directory: str = 'cache', expire: int = 60 * 60 * 24):
    cache = Cache(directory=directory)
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = func.__name__ + ':' + hashlib.md5((func.__name__ + str(args) + str(kwargs)).encode('utf-8')).hexdigest()
            result = cache.get(key)
            if result is not None:
                return result
            result = func(*args, **kwargs)
            cache.set(key, result, expire)
            return result
        return wrapper
    return decorator
