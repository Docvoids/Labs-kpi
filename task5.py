import asyncio

class MessageBus:
    def __init__(self):
        self._subscribers = {}

    async def subscribe(self, message_type, callback):
        # Added check if callback is a coroutine
        if not asyncio.iscoroutinefunction(callback):
            raise ValueError("Callback must be an asynchronous function (coroutine)")
        if message_type not in self._subscribers:
            self._subscribers[message_type] = []
        self._subscribers[message_type].append(callback)

    async def publish(self, message_type, message_data):
        if message_type in self._subscribers:
            # Using asyncio.gather to execute all handlers concurrently
            await asyncio.gather(*(subscriber(message_data) for subscriber in self._subscribers[message_type]))

class Entity:
    def __init__(self, name, message_bus):
        self.name = name
        self.message_bus = message_bus

    async def publish_message(self, message_type, data):
        print(f"{self.name}: Publishing message of type '{message_type}' with data: {data}")
        await self.message_bus.publish(message_type, data)

    async def handle_user_created(self, user_data):
        print(f"{self.name}: Handling user created event: {user_data}")

    async def handle_order_placed(self, order_data):
        print(f"{self.name}: Handling order placed event: {order_data}")

async def main():
    bus = MessageBus()
    entity_a = Entity("Entity A", bus)
    entity_b = Entity("Entity B", bus)

    # Subscribe Entity methods to specific message types
    await bus.subscribe("event.user.created", entity_a.handle_user_created)
    await bus.subscribe("event.order.placed", entity_b.handle_order_placed)
    await bus.subscribe("event.user.created", entity_b.handle_user_created) # Entity B is also subscribed to user creation

    await entity_a.publish_message("event.user.created", {"user_id": 123, "username": "test_user"})
    await entity_b.publish_message("event.order.placed", {"order_id": 456, "total": 100})

if __name__ == "__main__":
    asyncio.run(main())