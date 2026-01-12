"""
Items service - работа с базой предметов Stalcraft
"""

# import httpx
# from typing import Any
from app.config import settings
from app.models.items import Item, ItemsListResponse

# from app.core.exceptions import ItemNotFoundError


class ItemsService:
    """Сервис для работы с базой предметов"""

    def __init__(self):
        self.github_base_url = settings.github_db_base_url

    async def get_item(self, item_id: str, realm: str = "global") -> Item:
        """
        Получить информацию о предмете из GitHub базы

        TODO: Реализовать после изучения структуры stalcraft-database
        """
        # Временная заглушка
        return Item(
            id=item_id,
            name=f"Item {item_id}",
            category="unknown",
            subcategory="unknown",
        )

    async def search_items(
        self, query: str, realm: str = "global"
    ) -> ItemsListResponse:
        """
        Поиск предметов по названию

        TODO: Реализовать после изучения структуры stalcraft-database
        """
        # Временная заглушка
        return ItemsListResponse(items=[], total=0)

    async def list_items(
        self, category: str | None = None, realm: str = "global"
    ) -> ItemsListResponse:
        """
        Получить список предметов

        TODO: Реализовать после изучения структуры stalcraft-database
        """
        # Временная заглушка
        return ItemsListResponse(items=[], total=0)


# Singleton
items_service = ItemsService()
