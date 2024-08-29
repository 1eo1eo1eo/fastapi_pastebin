import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.config import settings
from core.models import db_helper

from auth.views import router as authentication_router
from auth.actions.create_superuser import create_superuser


@asynccontextmanager
async def lifespan(main_app: FastAPI):
    # startup
    await create_superuser()
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
    title="Pastebin",
)

main_app.include_router(authentication_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
