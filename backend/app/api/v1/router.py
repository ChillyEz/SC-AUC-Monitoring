"""
Main API v1 router
"""
from fastapi import APIRouter
from app.api.v1 import auction, items

api_router = APIRouter()

# Include sub-routers
api_router.include_router(auction.router)
api_router.include_router(items.router)


@api_router.get("/")
async def api_root():
    """API v1 root endpoint"""
    return {
        "message": "SC-AUC-Monitoring API v1",
        "endpoints": {
            "auction": "/auction",
            "items": "/items",
            "docs": "/api/docs"
        }
    }
