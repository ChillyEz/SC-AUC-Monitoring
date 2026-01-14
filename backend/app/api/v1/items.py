"""
Items API endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from app.services.items_service import items_service
from app.models.items import ItemsListResponse


router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/search", response_model=ItemsListResponse)
async def search_items(
    query: str = Query(..., min_length=1, description="Поисковый запрос"),
    realm: str = Query(default="global", description="Realm (global, ru)"),
    limit: int = Query(
        default=20, ge=1, le=100, description="Максимальное количество результатов"
    ),
):
    """
    Поиск предметов по названию

    - **query**: Поисковый запрос
    - **realm**: Realm (global или ru)
    - **limit**: Максимальное количество результатов (1-100)
    """
    try:
        return await items_service.search_items(query, realm, limit)
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


@router.get("/{item_id}", response_model=ItemsListResponse)
async def get_item(
    item_id: str,
    realm: str = Query(default="global", description="Realm (global, ru)"),
):
    """
    Получить информацию о предмете

    - **item_id**: ID предмета
    - **realm**: Realm (global или ru)
    """
    try:
        result = await items_service.get_item(item_id, realm)
        if result.total == 0:
            raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.post("/update-database")
async def update_database(
    realms: list[str] = Query(default=["ru", "global"]),
):
    """
    Обновить локальную базу данных предметов (может занять несколько минут)

    - **realms**: Список realms для обновления (по умолчанию ["ru", "global"])
    """
    try:
        await items_service.update_database(realms)
        return {
            "status": "success",
            "message": f"Database updated for realms: {', '.join(realms)}",
            "total_items": items_service.db_manager.get_total_items(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")
