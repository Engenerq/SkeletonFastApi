from fastapi import APIRouter
from app.web.api.v1.wallets.router import router as wallets_router

router = APIRouter(
    prefix='/v1'
)

router.include_router(wallets_router)
