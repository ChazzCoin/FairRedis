import json
import redis
from F import DICT

# redis-cli -h 192.168.1.229 -p 6379 -a <password>
# host='192.168.1.229'
# port=6379
# db=0
# -> pubsub {'type': 'message', 'pattern': None, 'channel': b'channel-1', 'data': b'this is a dykw message!'}
class Redis:
    client = None
    runPoller = False
    enablePubSub = False
    pubsub_client = None
    channels = []
    messages = {}
    pubsub_callback = None

    def __init__(self, **kwargs):
        if kwargs:
            ip = DICT.get("ip", kwargs, default=False)
            host = DICT.get("host", kwargs, default=False)
            port = DICT.get("port", kwargs, default=False)
            db = DICT.get("db", kwargs, default=False)
            self.enablePubSub = DICT.get("enablePubSub", kwargs, default=False)
            self.connect_to_redis(host=host if not ip else ip, port=port, db=db)

    def connect_to_redis(self, host:str, port:int, db:int):
        self.client = redis.Redis(host=host, port=port, db=db)
        return self

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
            return self.get_dict(key)
        return self.client.get(key)

    def get_dict(self, key):
        result = self.client.get(key)
        result = self.parse_str_to_dict(result)
        return result

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
