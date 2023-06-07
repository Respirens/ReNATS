# ReNats

> Elegant, modern and asynchronous NATS Client API framework in Python

```python
from renats.client import connect


client = await connect('127.0.0.1', 4222)

# Publish message to subject 'my.subject' with payload 'My payload =)'
await client.publish('my.subject', b'My payload =)')

# Publish message to subject 'my.subject' with payload 'My payload =)',
# reply subject 'my.reply.subject' and header 'MyHeader' with value 'MyValue'
await client.publish('my.subject', b'My payload =)', reply='my.reply.subject', headers={'MyHeader': 'MyValue'})

# Closing client
await client.close()
```

---

### TODO
- Subscriptions
- JetStream
- ObjectStorage
- Request-Reply
- Request-Reply API Framework for microservices
- And more, maybe...
