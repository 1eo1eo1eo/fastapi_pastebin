from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from core.config import settings
from core.models import db_helper


@asynccontextmanager
async def lifespan(main_app: FastAPI):
    #startup
    yield
    #shutdown
    await db_helper.dispose()

main_app = FastAPI(
    lifespan=lifespan
)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )