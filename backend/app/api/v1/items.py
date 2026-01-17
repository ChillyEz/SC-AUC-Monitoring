"""
Items API endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from app.services.items_service import items_service
from app.models.items import ItemSearchResult, ItemsListResponse
from app.core.exceptions import ItemNotFoundError

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/search", response_model=ItemsListResponse)
async def search_items(
    query: str = Query(..., min_length=1, description="Поисковый запрос"),
    realm: str = Query(default="ru", description="Realm (ru, global)"),
    limit: int = Query(default=20, ge=1, le=100, description="Максимум результатов"),
):
    """
    Быстрый поиск предметов в локальной базе

    - **query**: Поисковый запрос (название или ID)
    - **realm**: Регион (ru или global)
    - **limit**: Максимальное количество результатов
    """
    try:
        return await items_service.search_items(query, realm, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@router.get("/{item_id}", response_model=ItemSearchResult)
async def get_item(
    item_id: str,
    realm: str = Query(default="ru", description="Realm (ru, global)"),
):
    """
    Получить информацию о предмете по ID

    - **item_id**: ID предмета
    - **realm**: Регион
    """
    try:
        return await items_service.get_item(item_id, realm)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.post("/update-database")
async def update_database(
    realms: list[str] = Query(default=["ru", "global"], description="Realms to update"),
):
    """
    Обновить локальную базу данных предметов

    **Внимание**: Эта операция может занять несколько минут!

    - **realms**: Список регионов для обновления
    """
    try:
        await items_service.update_database(realms)
        return {
            "status": "success",
            "message": f"Database updated for realms: {', '.join(realms)}",
            "total_items": sum(
                len(items) for items in items_service.db_manager.search_index.values()
            ),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")
