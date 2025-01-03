import asyncio

class MessageBus:
    def __init__(self):
        self._subscribers = {}

    async def subscribe(self, message_type, callback):
        if message_type not in self._subscribers:
            self._subscribers[message_type] = []
        self._subscribers[message_type].append(callback)

    async def publish(self, message_type, message_data):
        if message_type in self._subscribers:
            for subscriber in self._subscribers[message_type]:
                await subscriber(message_data)

class Entity:
    def __init__(self, name, message_bus):
        self.name = name
        self.message_bus = message_bus

    async def publish_message(self, message_type, data):
        print(f"{self.name}: Publishing message of type '{message_type}' with data: {data}")
        await self.message_bus.publish(message_type, data)

    async def handle_message(self, data):
        print(f"{self.name}: Received message: {data}")

async def entity_a_handler(data):
    print(f"Entity A handler received data: {data}")

async def entity_b_handler(data):
    print(f"Entity B handler received data: {data}")

async def main():
    bus = MessageBus()
    entity_a = Entity("Entity A", bus)
    entity_b = Entity("Entity B", bus)

    # Subscribe handlers to specific message types
    await bus.subscribe("event.user.created", entity_a_handler)
    await bus.subscribe("event.order.placed", entity_b_handler)

    await entity_a.publish_message("event.user.created", {"user_id": 123, "username": "test_user"})
    await entity_b.publish_message("event.order.placed", {"order_id": 456, "total": 100})

if __name__ == "__main__":
    asyncio.run(main())