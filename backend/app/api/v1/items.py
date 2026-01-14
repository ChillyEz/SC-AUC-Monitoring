"""
Items API endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from app.services.items_service import items_service
from app.models.items import Item, ItemsListResponse
from app.core.exceptions import ItemNotFoundError

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/search", response_model=ItemsListResponse)
async def search_items(
    query: str = Query(..., min_length=1, description="Поисковый запрос"),
    realm: str = Query(default="global", description="Realm (global, ru)"),
):
    """
    Поиск предметов по названию

    - **query**: Поисковый запрос
    - **realm**: Realm (global или ru)
    """
    try:
        return await items_service.search_items(query, realm)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/list", response_model=ItemsListResponse)
async def list_items(
    category: str | None = Query(default=None, description="Категория"),
    realm: str = Query(default="global", description="Realm (global, ru)"),
):
    """
    Получить список предметов

    - **category**: Фильтр по категории (опционально)
    - **realm**: Realm (global или ru)
    """
    try:
        return await items_service.list_items(category, realm)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/{item_id}", response_model=Item)
async def get_item(
    item_id: str,
    category: str = Query(..., description="Категория предмета (weapon/pistol, etc)"),
    realm: str = Query(default="global", description="Realm (global, ru)"),
):
    """
    Получить информацию о предмете

    - **item_id**: ID предмета
    - **category**: Категория предмета
    - **realm**: Realm (global или ru)
    """
    try:
        return await items_service.get_item(item_id, category, realm)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
