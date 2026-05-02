## An example of using multiple brokers

FastStream is a convenient syntactic sugar layer that provides a clean and unified interface for working with popular message and event brokers such as RabbitMQ, Kafka, NATS, and others. It allows you to abstract away low-level details and focus on business logic using a declarative style for subscribers and publishers.

Let’s look at a simple example with a single broker:

```python
from faststream import FastStream
from faststream.rabbit import RabbitBroker

broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
app = FastStream(broker)

@broker.subscriber("orders")
async def handle_order(msg: dict):
    print(msg)
```

However, if you need to connect an additional broker but cannot allocate a separate container for it, or if you need to work with multiple isolated queues (for example, different RabbitMQ instances) within a single service, or you want to separate responsibility domains (e.g., internal vs external events) without splitting into multiple processes — you end up needing multiple brokers in a single Docker container.

In such cases, FastStream provides a way to use multiple brokers with a single entry point. Let’s look at an example:

```python
from contextlib import asynccontextmanager
from faststream import FastStream
from faststream.rabbit import RabbitBroker

# Primary broker
main_broker = RabbitBroker("amqp://guest:guest@localhost:5672/")

# Secondary broker
secondary_broker = RabbitBroker("amqp://guest:guest@localhost:5673/")

@asynccontextmanager
async def lifespan():
    # manually start the secondary broker
    await secondary_broker.start()
    try:
        yield
    finally:
        await secondary_broker.close()

# main broker is managed by FastStream
app = FastStream(main_broker, lifespan=lifespan)

# primary broker handler
@main_broker.subscriber("main_queue")
async def handle_main(msg: dict):
    print(f"[MAIN] {msg}")

# secondary broker handler
@secondary_broker.subscriber("secondary_queue")
async def handle_secondary(msg: dict):
    print(f"[SECONDARY] {msg}")

# example publishing
@app.after_startup
async def publish_messages():
    await main_broker.publish({"msg": "hello main"}, "main_queue")
    await secondary_broker.publish({"msg": "hello secondary"}, "secondary_queue")
```
