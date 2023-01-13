import json
import redis

import F
from F import DICT
from F.CLASS import Flass
from F.TYPE.Dict import fict

# redis-cli -h 192.168.1.xxx -p 6379 -a <password>
# host='192.168.1.xxx'
# port=6379
# db=0
# -> pubsub {'type': 'message', 'pattern': None, 'channel': b'channel-1', 'data': b'this is a dykw message!'}
BASE_KEY = lambda service, attribute: f"{service}:{attribute}"
CONFIG_KEY = lambda name: BASE_KEY(name, "config")
CONFIG_MODEL = { "host": "", "ip": "", "port": "", "db": "", "username": "", "password": "" }
class Redis(Flass):
    username = ""
    password = ""
    host = "localhost"
    ip = "127.0.0.1"
    port = 6379
    db = 0
    client = None
    runPoller = False
    enablePubSub = False
    pubsub_client = None
    channels = []
    messages = {}
    pubsub_callback = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect_to_redis()

    def connect_to_redis(self):
        self.client = redis.Redis(host=self._host(), port=self.port, db=self.db)
        # self.client = redis.Redis(host=self._host(), port=self.port, db=self.db, username=self.username, password=self.password)
        return self

    def _host(self):
        return F.ifElse(self.ip, self.host)

    def set(self, key, value):
        if type(value) not in [str]:
            value = str(value)
        return self.client.set(key, value)

    def add(self, key, value):
        if type(value) not in [str]:
            value = str(value)
        return self.client.set(key, value)

    def get(self, key, parseDict=False):
        if parseDict:
            return self.get_fict(key)
        return self.client.get(key)

    def get_config(self, key):
        return self.get_fict(CONFIG_KEY(key))

    def get_fict(self, key):
        result = self.client.get(key)
        result = self.parse_str_to_dict(result)
        return fict(result)

    @staticmethod
    def parse_str_to_dict(value):
        result = value.decode().replace("'", "\"")
        result = json.loads(result)
        return result

    def remove(self, key):
        return self.client.delete(key)

    def contains(self, key):
        results = self.get(key)
        if results:
            return True
        return False

    """
        - PubSub
    """
    def enable_PubSub(self):
        self.enablePubSub = True
        self.set_pub_client()

    def set_pub_client(self):
        self.pubsub_client = self.client.pubsub()

    def publish_message(self, channel, message):
        self.client.publish(channel, message)

    def subscribe(self, channelName):
        self.pubsub_client.subscribe(channelName)
        self.listen_for_messages()
        self.channels.append(channelName)

    def listen_for_messages(self):
        for message in self.pubsub_client.listen():
            channel = DICT.get("channel", message, default=False)
            message = DICT.get("data", message, default=False)
            response = f"{channel}: {message}"
            print(response)
            self.messages[channel] = message
            if self.pubsub_callback:
                self.pubsub_callback(message)

if __name__ == '__main__':
    r = Redis(ip="192.168.1.229")
    CONFIG_MODEL["ip"] = "192.168.1.xxx"
    CONFIG_MODEL["host"] = "192.168.1.xxx"
    CONFIG_MODEL["port"] = "6379"
    CONFIG_MODEL["db"] = "0"
    CONFIG_MODEL["username"] = ""
    CONFIG_MODEL["password"] = ""
    r.set(CONFIG_KEY("redis"), CONFIG_MODEL)