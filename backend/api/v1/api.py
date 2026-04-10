from fastapi import APIRouter

from backend.api.v1.endpoints import (
    analytics, buildings, catalog, dispatch, inventory, 
    login, operations, orders, purchase, superadmin, users, media, transfers
)

api_router = APIRouter()
api_router.include_router(login.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(superadmin.router, prefix="/superadmin", tags=["superadmin"])
api_router.include_router(operations.router, prefix="/operations", tags=["operations"])
api_router.include_router(catalog.router, prefix="/catalog", tags=["catalog"])
api_router.include_router(buildings.router, prefix="/buildings", tags=["buildings"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(purchase.router, prefix="/purchases", tags=["purchases"])
api_router.include_router(dispatch.router, prefix="/dispatch", tags=["dispatch"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(media.router, prefix="/media", tags=["media"])
api_router.include_router(transfers.router, prefix="/transfers", tags=["transfers"])
