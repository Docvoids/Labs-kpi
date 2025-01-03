import asyncio
from typing import Callable, List, TypeVar, Any, Coroutine

T = TypeVar('T')
U = TypeVar('U')

async def async_map(
    fn: Callable[[T], Coroutine[Any, Any, U]],
    data: List[T]
) -> List[U]:
    tasks = [fn(item) for item in data]
    return await asyncio.gather(*tasks)

async def async_filter(
    predicate: Callable[[T], Coroutine[Any, Any, bool]],
    data: List[T]
) -> List[T]:
    async def check(item):
        if await predicate(item):
            return item
        return None
    tasks = [check(item) for item in data]
    results = await asyncio.gather(*tasks)
    return [item for item in results if item is not None]

async def async_filter_map(
    fn: Callable[[T], Coroutine[Any, Any, U | None]],
    data: List[T]
) -> List[U]:
    tasks = [fn(item) for item in data]
    results = await asyncio.gather(*tasks)
    return [item for item in results if item is not None]

async def async_some(
    predicate: Callable[[T], Coroutine[Any, Any, bool]],
    data: List[T]
) -> bool:
    async def check(item):
        if await predicate(item):
            raise StopAsyncIteration()
        return False
    tasks = [check(item) for item in data]
    try:
        await asyncio.gather(*tasks)
        return False
    except StopAsyncIteration:
        return True

async def async_find(
    predicate: Callable[[T], Coroutine[Any, Any, bool]],
    data: List[T]
) -> T | None:
    async def check(item):
        if await predicate(item):
            return item
        return None
    for item in data:
        result = await check(item)
        if result is not None:
            return result
    return None

async def async_find_index(
    predicate: Callable[[T], Coroutine[Any, Any, bool]],
    data: List[T]
) -> int | None:
    async def check(item):
        return await predicate(item)
    for index, item in enumerate(data):
        if await check(item):
            return index
    return None

def debounce(delay: float):
    def decorator(func: Callable[..., Coroutine[Any, Any, U]]):
        _task = None
        async def debounced(*args: Any, **kwargs: Any) -> None:
            nonlocal _task
            if _task:
                _task.cancel()
            _task = asyncio.create_task(_DebouncedRunner(func, delay, *args, **kwargs).run())
        return debounced
    return decorator

class _DebouncedRunner:
    def __init__(self, func: Callable[..., Coroutine[Any, Any, U]], delay: float, *args: Any, **kwargs: Any):
        self.func = func
        self.delay = delay
        self.args = args
        self.kwargs = kwargs
    async def run(self) -> None:
        await asyncio.sleep(self.delay)
        await self.func(*self.args, **self.kwargs)

async def my_async_map_callback(x: int) -> str:
    await asyncio.sleep(0.1)
    return f"Mapped: {x * 2}"

async def my_async_filter_predicate(x: int) -> bool:
    await asyncio.sleep(0.05)
    return x > 3

async def my_async_filter_map_callback(x: int) -> str | None:
    await asyncio.sleep(0.08)
    if x % 2 == 0:
        return f"FilterMapped: {x}"
    return None

async def my_async_some_predicate(x: int) -> bool:
    await asyncio.sleep(0.03)
    return x == 5

async def my_async_find_predicate(x: int) -> bool:
    await asyncio.sleep(0.07)
    return x > 4

async def my_async_find_index_predicate(x: int) -> bool:
    await asyncio.sleep(0.09)
    return x == 3

async def debounced_function(x: int) -> None:
    print(f"Debounced function called with: {x}")

@debounce(0.3)
async def debounced_async_function(x: int) -> None:
    print(f"Debounced async function called with: {x}")

async def main():
    data = [1, 2, 3, 4, 5]

    print("--- async_map ---")
    mapped_data = await async_map(my_async_map_callback, data)
    print(mapped_data)

    print("\n--- async_filter ---")
    filtered_data = await async_filter(my_async_filter_predicate, data)
    print(filtered_data)

    print("\n--- async_filter_map ---")
    filter_mapped_data = await async_filter_map(my_async_filter_map_callback, data)
    print(filter_mapped_data)

    print("\n--- async_some ---")
    has_some = await async_some(my_async_some_predicate, data)
    print(has_some)

    print("\n--- async_find ---")
    found_item = await async_find(my_async_find_predicate, data)
    print(found_item)

    print("\n--- async_find_index ---")
    found_index = await async_find_index(my_async_find_index_predicate, data)
    print(found_index)

    print("\n--- debounce (synchronous function) ---")
    debounced_sync = debounce(0.2)(lambda x: print(f"Debounced sync called with: {x}"))
    debounced_sync(1)
    debounced_sync(2)
    await asyncio.sleep(0.1)
    debounced_sync(3)
    await asyncio.sleep(0.5)

    print("\n--- debounce (asynchronous function) ---")
    await debounced_async_function(1)
    await debounced_async_function(2)
    await asyncio.sleep(0.1)
    await debounced_async_function(3)
    await asyncio.sleep(0.5)

if __name__ == "__main__":
    asyncio.run(main())