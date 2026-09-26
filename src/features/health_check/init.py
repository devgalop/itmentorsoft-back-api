from fastapi import APIRouter

from src.features.health_check.health_check_endpoint import (
    router as health_check_router,
)

router = APIRouter()
router.include_router(health_check_router)
