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