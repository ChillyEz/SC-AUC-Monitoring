"""
Items service - работа с базой предметов Stalcraft
"""

from app.services.items_database_manager import items_db_manager
from app.models.items import ItemSearchResult, ItemsListResponse
from app.core.exceptions import ItemNotFoundError


class ItemsService:
    """Сервис для работы с базой предметов"""

    def __init__(self):
        self.db_manager = items_db_manager

    async def search_items(
        self, query: str, realm: str = "ru", limit: int = 20
    ) -> ItemsListResponse:
        """
        Быстрый поиск предметов в локальной базе

        Args:
            query: Поисковый запрос
            realm: Регион (ru, global)
            limit: Максимальное количество результатов
        """
        results = self.db_manager.search(query, realm, limit)

        items = [
            ItemSearchResult(
                id=item["id"],
                name=item["name"],
                category=item["category"],
                icon_url=item["icon_url"],
            )
            for item in results
        ]

        return ItemsListResponse(items=items, total=len(items))

    async def get_item(self, item_id: str, realm: str = "ru") -> ItemSearchResult:
        """
        Получить информацию о предмете по ID

        Args:
            item_id: ID предмета
            realm: Регион
        """
        item = self.db_manager.get_item_by_id(item_id, realm)

        if not item:
            raise ItemNotFoundError(f"Item {item_id} not found")

        return ItemSearchResult(
            id=item["id"],
            name=item["name"],
            category=item["category"],
            icon_url=item["icon_url"],
        )

    async def update_database(self, realms:  list[str] | None = None):
        """
        Обновить локальную базу данных

        Args:
            realms:  Список регионов для обновления
        """
        await self.db_manager.update_database(realms)


# Singleton
items_service = ItemsService()
