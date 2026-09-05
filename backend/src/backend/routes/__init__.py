from fastapi import APIRouter

from .create_transaction import router as create_router
from .delete_transaction import router as delete_router
from .get_rating import router as rating_router
from .get_summary import router as summary_router
from .get_transaction import router as get_router
from .list_transactions import router as list_router
from .update_transaction import router as update_router

router = APIRouter()
router.include_router(create_router)
router.include_router(delete_router)
router.include_router(rating_router)
router.include_router(summary_router)
router.include_router(get_router)
router.include_router(list_router)
router.include_router(update_router)

__all__ = ["router"]
