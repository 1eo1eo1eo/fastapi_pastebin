from fastapi import APIRouter

from .api_v1.views import router as messages_router


router = APIRouter(
    prefix="/api",
)

router.include_router(
    router=messages_router,
)
