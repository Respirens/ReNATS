# ReNATS

> Elegant, modern and asynchronous NATS Client API library written in pure Python

```python
import asyncio
from renats.client import NATSClient, Message

servers = (
    ("127.0.0.1", 4222),
)

client = await NATSClient().connect(servers)

# Publish message to subject 'my.subject' with payload 'My payload =)'
await client.publish("my.subject", b"My payload =)")

# Publish message to subject 'my.subject' with payload 'My payload =)',
# reply subject 'my.reply.subject' and header 'MyHeader' with value 'MyValue'
await client.publish(
    subject="my.subject",
    payload=b"My payload =)",
    reply_subject="my.reply.subject",
    headers={
        "MyHeader": "MyValue"
    }
)


# Callbacks can be sync or async (def or async def)
def callback(message: Message):
    print(f"Received message in sync callback from {message.subject}: {message.payload}")


async def async_callback(message: Message):
    await asyncio.sleep(3)
    print(f"Received message in async callback from {message.subject}: {message.payload}")


subscription = await client.subscribe("foo.bar", callback)
another_subscription = await client.subscribe("foo.baz", async_callback)

await client.publish("foo.bar", b"Hello world! (to subscription with sync callback)")
await client.publish("foo.baz", b"Hello world! (to subscription with async callback)")

await subscription.unsubscribe()
await another_subscription.unsubscribe()

# Closing client
await client.close()
```

### Installation
```bash
pip install renats
```

### TODO
- JetStream
- ObjectStorage
- Request-Reply API Framework for microservices
- And more, maybe...
