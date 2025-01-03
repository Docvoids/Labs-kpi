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