from functools import wraps
from fastapi.responses import StreamingResponse
from Flux import Flux

def sse_stream(model=None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            flux = await func(*args, **kwargs)
            flux = flux.map(lambda o: o.model_dump() if isinstance(o, model) else o).to_sse()
            
            return StreamingResponse(
                flux, 
                media_type="text/event-stream"
            )
        return wrapper
    return decorator