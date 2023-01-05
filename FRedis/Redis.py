import redis
from F import DICT

# host='192.168.1.229'
# port=6379
# db=0

class Redis:
    client = None

    def __init__(self, **kwargs):
        if kwargs:
            ip = DICT.get("ip", kwargs, default=False)
            host = DICT.get("host", kwargs, default=False)
            port = DICT.get("port", kwargs, default=False)
            db = DICT.get("db", kwargs, default=False)
            self.connect_to_redis(host=host if not ip else ip, port=port, db=db)

    def connect_to_redis(self, host:str, port:int, db:int):
        self.client = redis.Redis(host=host, port=port, db=db)
        return self

    def set(self, key, value):
        return self.client.set(key, value)

    def add(self, key, value):
        return self.client.set(key, value)

    def get(self, key):
        return self.client.get(key)

    def remove(self, key):
        return self.client.delete(key)

    def contains(self, key):
        results = self.get(key)
        if results:
            return True
        return False


r = Redis().connect_to_redis("192.168.1.229", 6379, 0)
print(r.contains("testing"))
r.remove("testing")
print(r.contains("testing"))