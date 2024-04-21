from fastapi import APIRouter
from .login import router as login_router
from .company import router as company_router
from .templatest import router as template_router


router = APIRouter(prefix="/v1")
router.include_router(login_router)
router.include_router(company_router)
router.include_router(template_router)