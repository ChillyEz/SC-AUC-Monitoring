"""
Auction API endpoints
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Literal
from app.models.auction import (
    AuctionLotsResponse,
    AuctionHistoryResponse,
    AuctionSortField,
    SortOrder,
)
from app.services.auction_service import auction_service
from app.core.exceptions import StalcraftAPIError, InvalidRegionError

router = APIRouter(prefix="/auction", tags=["Auction"])

Region = Literal["eu", "ru", "na", "sea"]


@router.get(
    "/{region}/{item_id}/lots",
    response_model=AuctionLotsResponse,
    summary="Получить активные лоты",
    description="Возвращает список активных лотов для указанного предмета на аукционе",
)
async def get_auction_lots(
    region: Region,
    item_id: str,
    additional: bool = Query(
        default=False, description="Включить дополнительную информацию"
    ),
    limit: int = Query(
        default=20, ge=0, le=200, description="Количество лотов (0-200)"
    ),
    offset: int = Query(default=0, ge=0, description="Сдвиг в списке"),
    order: SortOrder = Query(default="desc", description="Порядок сортировки"),
    sort: AuctionSortField = Query(
        default="time_created", description="Поле для сортировки"
    ),
):
    """
    Получить активные лоты аукциона

    - **region**: Регион игры (EU, RU, NA, SEA)
    - **item_id**: ID предмета (например, "y1q9")
    - **additional**: Включить дополнительную информацию о лотах
    - **limit**: Количество лотов в ответе (макс 200)
    - **offset**: Пропустить N лотов (для пагинации)
    - **order**: asc (возрастание) или desc (убывание)
    - **sort**: Поле для сортировки
      (time_created, time_left, current_price, buyout_price)
    """
    try:
        return await auction_service.get_lots(
            region=region,
            item_id=item_id,
            additional=additional,
            limit=limit,
            offset=offset,
            order=order,
            sort=sort,
        )
    except InvalidRegionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except StalcraftAPIError as e:
        raise HTTPException(status_code=502, detail=f"Stalcraft API error: {str(e)}")


@router.get(
    "/{region}/{item_id}/history",
    response_model=AuctionHistoryResponse,
    summary="Получить историю продаж",
    description="Возвращает историю цен для предмета, отсортированную по времени покупки",
)
async def get_auction_history(
    region: Region,
    item_id: str,
    additional: bool = Query(
        default=False, description="Включить дополнительную информацию"
    ),
    limit: int = Query(
        default=20, ge=0, le=200, description="Количество записей (0-200)"
    ),
    offset: int = Query(default=0, ge=0, description="Сдвиг в списке"),
):
    """
    Получить историю продаж предмета

    - **region**: Регион игры (EU, RU, NA, SEA)
    - **item_id**: ID предмета (например, "y1q9")
    - **additional**: Включить дополнительную информацию о продажах
    - **limit**: Количество записей в ответе (макс 200)
    - **offset**: Пропустить N записей (для пагинации)
    """
    try:
        return await auction_service.get_history(
            region=region,
            item_id=item_id,
            additional=additional,
            limit=limit,
            offset=offset,
        )
    except InvalidRegionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except StalcraftAPIError as e:
        raise HTTPException(status_code=502, detail=f"Stalcraft API error: {str(e)}")
