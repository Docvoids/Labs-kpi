import asyncio

class AbortController:
    def __init__(self):
        self._signal = asyncio.Future()

    def abort(self):
        if not self._signal.done():
            self._signal.set_result(None)

    async def signal(self):
        return await self._signal

async def my_async_task(controller):
    print("Task started")
    print("Task finished")

async def main():
    controller = AbortController()
    task = asyncio.create_task(my_async_task(controller))
    await task

if __name__ == "__main__":
    asyncio.run(main())