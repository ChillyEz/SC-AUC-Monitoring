"""
Items service - работа с базой предметов Stalcraft
"""

from app.clients.items_database import items_db_client
from app.models.items import Item, ItemsListResponse


class ItemsService:
    """Сервис для работы с базой предметов"""

    def __init__(self):
        self.db_client = items_db_client

    async def get_item(self, item_id: str, category: str, realm: str = "ru") -> Item:
        """
        Получить информацию о предмете из GitHub базы

        Args:
            item_id: ID предмета
            category: Категория предмета
            realm: Realm (по умолчанию "ru")

        Returns:
            Item object

        Raises:
            ItemNotFoundError: Если предмет не найден
        """
        return await self.db_client.fetch_item(item_id, category, realm)

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
            results = await self.db_client.search_items(query, realm, limit)
            return ItemsListResponse(items=results, total=len(results))
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
                results = await self.db_client.list_category_items(category, realm)
            else:
                # List items from all categories
                results = []
                for cat in self.db_client.categories:
                    try:
                        cat_items = await self.db_client.list_category_items(cat, realm)
                        results.extend(cat_items)
                    except Exception:
                        continue
            return ItemsListResponse(items=results, total=len(results))
        except Exception:
            # Return empty results on error
            return ItemsListResponse(items=[], total=0)


# Singleton
items_service = ItemsService()
