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