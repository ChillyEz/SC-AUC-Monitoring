"""
Items service - работа с базой предметов Stalcraft
"""

from app.models.items import ItemsListResponse
from app.services.items_database_manager import items_db_manager


class ItemsService:
    """Сервис для работы с базой предметов"""

    def __init__(self):
        self.db_manager = items_db_manager

    async def search_items(
        self, query: str, realm: str = "ru", limit: int = 20
    ) -> ItemsListResponse:
        """
        Поиск предметов по названию

        Args:
            query: Поисковый запрос
            realm: Realm (по умолчанию "ru")
            limit: Максимальное количество результатов

        Returns:
            ItemsListResponse with search results
        """
        try:
            results = self.db_manager.search(query, realm, limit)
            return ItemsListResponse(items=results, total=len(results))
        except Exception:
            # Return empty results on error
            return ItemsListResponse(items=[], total=0)

    async def get_item(self, item_id: str, realm: str = "ru") -> ItemsListResponse:
        """
        Получить информацию о предмете из локальной базы

        Args:
            item_id: ID предмета
            realm: Realm (по умолчанию "ru")

        Returns:
            ItemsListResponse with single item or empty

        Note:
            Changed to return ItemsListResponse for compatibility.
            Use search_items for full functionality.
        """
        try:
            item = self.db_manager.get_item_by_id(item_id, realm)
            if item:
                return ItemsListResponse(items=[item], total=1)
            return ItemsListResponse(items=[], total=0)
        except Exception:
            # Return empty results on error
            return ItemsListResponse(items=[], total=0)

    async def list_items(
        self, category: str | None = None, realm: str = "ru"
    ) -> ItemsListResponse:
        """
        Получить список предметов

        Args:
            category: Фильтр по категории (опционально)
            realm: Realm (по умолчанию "ru")

        Returns:
            ItemsListResponse with items
        """
        try:
            if category:
                # Filter by category
                results = [
                    item
                    for item in self.db_manager.search("", realm, limit=10000)
                    if item.category == category
                ]
            else:
                # Return all items
                results = self.db_manager.search("", realm, limit=10000)

            return ItemsListResponse(items=results, total=len(results))
        except Exception:
            # Return empty results on error
            return ItemsListResponse(items=[], total=0)

    async def update_database(self, realms: list[str] | None = None) -> None:
        """
        Обновить локальную базу данных предметов

        Args:
            realms: Список realms для обновления (по умолчанию ["ru", "global"])
        """
        await self.db_manager.update_database(realms)


# Singleton
items_service = ItemsService()
