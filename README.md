# ReNATS

> Elegant, modern and asynchronous NATS Client API library written in pure Python

```python
from renats.client import NATSClient


client = await NATSClient().connect("127.0.0.1", 4222)

# Publish message to subject 'my.subject' with payload 'My payload =)'
await client.publish("my.subject", b"My payload =)")

# Publish message to subject 'my.subject' with payload 'My payload =)',
# reply subject 'my.reply.subject' and header 'MyHeader' with value 'MyValue'
await client.publish(
    subject="my.subject",
    data=b"My payload =)",
    reply="my.reply.subject",
    headers={
        "MyHeader": "MyValue"
    }
)

# Closing client
await client.close()
```

### Installation
```bash
pip install renats
```

---

### TODO
- Subscriptions
- Request-Reply
- JetStream
- ObjectStorage
- Request-Reply API Framework for microservices
- And more, maybe...
