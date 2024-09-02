import uvicorn
from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from core.config import settings
from core.models import db_helper

from auth.views import router as authentication_router
from auth.actions.create_superuser import create_superuser

from api import router as messages_router


@asynccontextmanager
async def lifespan(main_app: FastAPI):
    # startup
    redis = aioredis.from_url(f"redis://{settings.redis.host}:{settings.redis.port}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    await create_superuser()
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
    title="Pastebin",
)

main_app.include_router(authentication_router)
main_app.include_router(messages_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
