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
    for i in range(5):
        print(f"Task working: {i}")
        try:
            await asyncio.sleep(1)
            await asyncio.wait_for(controller.signal(), timeout=0.001)
            print("Task received abort signal")
            break
        except asyncio.TimeoutError:
            pass
    print("Task finished")

async def main():
    controller = AbortController()
    task = asyncio.create_task(my_async_task(controller))
    await task

if __name__ == "__main__":
    asyncio.run(main())