from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from core.config import settings
from core.models import db_helper

from users.views import router as users_router
from auth.views import router as jwt_auth_router


@asynccontextmanager
async def lifespan(main_app: FastAPI):
    #startup
    yield
    #shutdown
    await db_helper.dispose()

main_app = FastAPI(
    lifespan=lifespan,
    title="Pastebin",
)

main_app.include_router(
    users_router,
)

main_app.include_router(
    jwt_auth_router,
)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )