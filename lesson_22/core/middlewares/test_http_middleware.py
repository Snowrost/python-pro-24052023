from starlette.middleware.base import BaseHTTPMiddleware
import time


class TestHttpMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        begin = time.time()
        response = await call_next(request)
        print(f"REQUEST TIME: {time.time() - begin} ms")
        return response
