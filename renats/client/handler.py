from renats.client.subscription import Subscription
from renats.connection.base import Connection
from renats.protocol.messages.msg import MsgProtocolMessage, HMsgProtocolMessage


class EventHandler:
    def __init__(self, connection: Connection):
        self._connection: Connection = connection
        self._subscriptions: dict[str, Subscription] = {}

    def add_subscription(self, sid: str, subscription: Subscription):
        self._subscriptions[sid] = subscription

    def delete_subscription(self, sid: str):
        del self._subscriptions[sid]

    def message(self, message: MsgProtocolMessage | HMsgProtocolMessage):
        pass
