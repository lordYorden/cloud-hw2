import json
from typing import Any, AsyncIterable, Callable
from aiostream import stream
from fastapi_pagination import Params

class Flux:
    def __init__(self, source: AsyncIterable):
        self._current_stream = stream.iterate(source)
        self._source = source
        
    def paginate(self, params: Params) -> "Flux":
        """
        Operator that applies FastAPI pagination parameters to the source.
        Works with Beanie/Pymongo queries.
        """
        # Convert page/size to MongoDB skip/limit
        # Params defaults to page 1, size 50
        limit = params.size
        skip = params.page * params.size
        
        if hasattr(self._source, "skip"):
            self._source = self._source.skip(skip)
        if hasattr(self._source, "limit"):
            self._source = self._source.limit(limit)
            
        return self

    def map(self, func: Callable[[Any], Any]) -> "Flux":
        self._current_stream = stream.map(self._current_stream, func)
        return self

    def filter(self, func: Callable[[Any], bool]) -> "Flux":
        self._current_stream = stream.filter(self._current_stream, func)
        return self

    def to_sse(self) -> AsyncIterable[str]:
        """
        Terminal operator: Returns a stream that formats items as SSE.
        This mimics Flux.map(toSSE).
        """
        # We wrap the existing stream in a mapper for SSE formatting
        self._current_stream = stream.map(
            self._current_stream,
            lambda x: f"data: {x if isinstance(x, str) else json.dumps(x)}\n\n"
        )
        # We return the aiostream object itself, which IS an AsyncIterable.
        return self

    async def __aiter__(self):
        """
        This allows the FluentStream object to be iterated directly:
        'async for x in fluent_stream:'
        """
        # aiostream requires a context manager to handle the lifecycle
        async with self._current_stream.stream() as streamer:
            async for item in streamer:
                yield item

def to_flux(iterable: AsyncIterable) -> Flux:
    return Flux(iterable)