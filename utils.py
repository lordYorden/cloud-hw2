from functools import wraps
from fastapi.responses import StreamingResponse
from Flux import Flux

def sse_stream(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # 1. Execute the function to get the FluentStream (Flux) object
        # Note: we check if the function itself is async or sync
        
        flux: Flux = None
        
        if any(f == func for f in [isinstance(func, type(lambda: None))]): # simple check
            flux = func(*args, **kwargs)
        else:
            flux = await func(*args, **kwargs)
             
        # 2. Return the StreamingResponse immediately
        return StreamingResponse(
            flux.to_sse(), 
            media_type="text/event-stream"
        )
    return wrapper