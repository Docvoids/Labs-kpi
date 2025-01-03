import asyncio

class MessageBus:
    def __init__(self):
        self._subscribers = {}

    async def subscribe(self, message_type, callback):
        if not asyncio.iscoroutinefunction(callback):
            raise ValueError("Callback must be an asynchronous function (coroutine)")
        if message_type not in self._subscribers:
            self._subscribers[message_type] = []
        self._subscribers[message_type].append(callback)
        return (message_type, callback) # Return subscription identifier for unsubscribing

    async def unsubscribe(self, subscription_id):
        message_type, callback = subscription_id
        if message_type in self._subscribers and callback in self._subscribers[message_type]:
            self._subscribers[message_type].remove(callback)
            print(f"Unsubscribed from '{message_type}': {callback.__name__}")

    async def publish(self, message_type, message_data):
        if message_type in self._subscribers:
            await asyncio.gather(*(subscriber(message_data) for subscriber in self._subscribers[message_type]))

class Entity:
    def __init__(self, name, message_bus):
        self.name = name
        self.message_bus = message_bus
        self.subscriptions = []

    async def subscribe_to(self, message_type, handler):
        subscription_id = await self.message_bus.subscribe(message_type, handler)
        self.subscriptions.append(subscription_id)

    async def unsubscribe_from_all(self):
        for subscription in self.subscriptions:
            await self.message_bus.unsubscribe(subscription)
        self.subscriptions = []

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

    # Subscribe through the Entity method
    await entity_a.subscribe_to("event.user.created", entity_a.handle_user_created)
    sub_b_order = await entity_b.subscribe_to("event.order.placed", entity_b.handle_order_placed)
    await entity_b.subscribe_to("event.user.created", entity_b.handle_user_created)

    await entity_a.publish_message("event.user.created", {"user_id": 123, "username": "test_user"})
    await entity_b.publish_message("event.order.placed", {"order_id": 456, "total": 100})

    # Unsubscribe Entity B from handling orders
    await bus.unsubscribe(sub_b_order)
    print("Entity B unsubscribed from handling orders.")

    await entity_b.publish_message("event.order.placed", {"order_id": 789, "total": 200}) # This message will no longer be handled by Entity B

    # Unsubscribe Entity A from all subscriptions
    await entity_a.unsubscribe_from_all()
    print("Entity A unsubscribed from all messages.")
    await entity_a.publish_message("event.user.created", {"user_id": 999, "username": "another_user"}) # This message will no longer be handled by Entity A

if __name__ == "__main__":
    asyncio.run(main())