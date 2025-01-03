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