import redis


class RedisHelper:

    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0, connection_pool=None)

    def set(self, key, value):
        self.redis.set(key, value)

    def get(self, key):
        self.redis.get(key)

    def hset(self, key, value, name='block2db'):
        self.redis.hset(name, key, value)

    def hget(self, key, name='block2db'):
        return self.redis.hget(name, key)
