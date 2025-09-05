import time
from typing import Callable
from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send


class RateLimitMiddleware:
    """Naive in-memory rate limit by (ip, path) per fixed window.

    Not for production scale, but fine for local/dev and basic protection.
    """

    def __init__(self, app: ASGIApp, limit: int = 60, window_seconds: int = 60):
        self.app = app
        self.limit = limit
        self.window = window_seconds
        self._store: dict[tuple[str, str], tuple[int, float]] = {}

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope)
        ip = request.client.host if request.client else "unknown"
        key = (ip, request.url.path)
        now = time.time()
        count, reset_at = self._store.get(key, (0, now + self.window))

        if now > reset_at:
            count = 0
            reset_at = now + self.window

        count += 1
        self._store[key] = (count, reset_at)

        if count > self.limit:
            from starlette.responses import JSONResponse

            await JSONResponse(
                {"detail": "rate limit exceeded"}, status_code=429, headers={
                    "X-RateLimit-Limit": str(self.limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(reset_at)),
                }
            )(scope, receive, send)
            return

        await self.app(scope, receive, send)


