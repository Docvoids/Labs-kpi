import asyncio
import random

async def fetch_data_promise(item_id):
    print(f"Promise: Starting to fetch data for item {item_id}")
    await asyncio.sleep(random.uniform(1, 3))
    result = f"Data for item {item_id}"
    print(f"Promise: Successfully fetched data for item {item_id}")
    return result

async def process_data_promise(item_id):
    future = asyncio.Future()
    asyncio.create_task(_set_future_result(future, item_id))
    data = await future
    print(f"Promise: Processing {data}")
    return f"Processed: {data}"

async def _set_future_result(future, item_id):
    result = await fetch_data_promise(item_id)
    future.set_result(result)

async def use_case_promise():
    print("Promise Use Case:")
    item_id = 1
    processed_data = await process_data_promise(item_id)
    print(f"Promise: Final processed data: {processed_data}")
    print("-" * 20)

async def fetch_data_async_await(item_id):
    print(f"Async/Await: Starting to fetch data for item {item_id}")
    await asyncio.sleep(random.uniform(1, 3))
    result = f"Data for item {item_id}"
    print(f"Async/Await: Successfully fetched data for item {item_id}")
    return result

async def process_data_async_await(item_id):
    data = await fetch_data_async_await(item_id)
    print(f"Async/Await: Processing {data}")
    return f"Processed: {data}"

async def use_case_async_await():
    print("Async/Await Use Case:")
    item_id = 1
    processed_data = await process_data_async_await(item_id)
    print(f"Async/Await: Final processed data: {processed_data}")
    print("-" * 20)

async def main():
    await use_case_promise()
    await use_case_async_await()

if __name__ == "__main__":
    asyncio.run(main())