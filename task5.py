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