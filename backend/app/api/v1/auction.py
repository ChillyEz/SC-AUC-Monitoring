"""
Auction API endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from app.services.auction_service import auction_service
from app.models.auction import AuctionLotsResponse, AuctionHistoryResponse
from app.core.exceptions import InvalidRegionError, StalcraftAPIError

router = APIRouter(prefix="/auction", tags=["Auction"])


@router.get("/{region}/{item_id}/lots", response_model=AuctionLotsResponse)
async def get_auction_lots(region: str, item_id: str):
    """
    Получить активные лоты аукциона

    - **region**: Регион (EU, RU, NA, SEA)
    - **item_id**: ID предмета
    """
    try:
        return await auction_service.get_lots(region, item_id)
    except InvalidRegionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except StalcraftAPIError as e:
        raise HTTPException(status_code=502, detail=f"Stalcraft API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/{region}/{item_id}/history", response_model=AuctionHistoryResponse)
async def get_auction_history(
    region: str,
    item_id: str,
    limit: int = Query(default=50, ge=1, le=100, description="Количество записей"),
):
    """
    Получить историю продаж

    - **region**: Регион (EU, RU, NA, SEA)
    - **item_id**: ID предмета
    - **limit**: Количество записей (1-100)
    """
    try:
        return await auction_service.get_history(region, item_id, limit)
    except InvalidRegionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except StalcraftAPIError as e:
        raise HTTPException(status_code=502, detail=f"Stalcraft API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
