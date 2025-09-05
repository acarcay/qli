from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.utils.rate_limit import RateLimitMiddleware
from app.api.routers import auth, menu, items, cart, orders, ai, analytics, search
from app.db.base import import_models


app = FastAPI(title="Qlick API")


@app.on_event("startup")
def on_startup() -> None:
    import_models()


app.add_middleware(RateLimitMiddleware, limit=60, window_seconds=60)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(menu.router)
app.include_router(items.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(ai.router)
app.include_router(analytics.router)
app.include_router(search.router)


