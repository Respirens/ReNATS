import asyncio
from asyncio import Future
from typing import Final

import uuid6

from renats.client.message import Message
from renats.client.base import NATS, HeadersType
from renats.client.subscription import Subscription

REQUESTS_INBOX_SUBJECT: Final[str] = "$_REQUESTS_INBOX.*"
REQUEST_REPLY_SUBJECT_TEMPLATE: Final[str] = REQUESTS_INBOX_SUBJECT + ".{request_id}"


class RequestManager:
    def __init__(self, client: NATS):
        self._client: NATS = client
        self._inbox_subscription: Subscription | None = None
        self._requests_pending: dict[str, Future[Message]] = {}

    @property
    def subscribed(self) -> bool:
        return self._inbox_subscription is not None

    def _create_callback(self):
        def callback(message: Message):
            request_id = message.subject.split(".")[1]
            request = self._requests_pending.pop(request_id, None)
            if request is None:
                return
            request.set_result(message)

        return callback

    async def subscribe(self):
        self._inbox_subscription = self._client.subscribe(REQUESTS_INBOX_SUBJECT, self._create_callback())

    async def unsubscribe(self):
        await self._inbox_subscription.unsubscribe()
        self._inbox_subscription = None

    async def request(
            self,
            subject: str,
            payload: bytes,
            headers: HeadersType | None,
            timeout: float | None
    ) -> Message:
        request_id = uuid6.uuid7().hex
        reply_subject = REQUEST_REPLY_SUBJECT_TEMPLATE.format(request_id=request_id)
        future = Future()
        self._requests_pending[request_id] = future

        await self._client.publish(subject, payload, reply_subject, headers)

        if timeout is None:
            return await future

        try:
            return await asyncio.wait_for(future, timeout)
        except Exception:
            del self._requests_pending[request_id]
            raise

