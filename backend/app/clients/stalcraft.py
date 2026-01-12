import httpx
from typing import Any, Literal
from app.config import settings
from app.core.exceptions import StalcraftAPIError


class StalcraftAPIClient:
    """
    Клиент для работы с Stalcraft API
    Поддерживает Demo и Production API

    ВАЖНО: Demo API тоже требует токен авторизации!
    """

    def __init__(self):
        self.base_url = settings.api_base_url
        self.timeout = 10.0

    def _get_headers(self) -> dict[str, str]:
        """
        Заголовки для запросов

        ВАЖНО: И Demo, и Production API требуют Authorization токен!
        """
        token = settings.api_token

        if not token:
            api_type = "Demo" if settings.USE_DEMO_API else "Production"
            raise StalcraftAPIError(
                f"{api_type} API token is required. "
                f"Set STALCRAFT_{'DEMO' if settings.USE_DEMO_API else 'PROD'}_TOKEN in .env"
            )

        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

    async def get_auction_lots(
        self,
        region: str,
        item_id: str,
        additional: bool = False,
        limit: int = 20,
        offset: int = 0,
        order: Literal["asc", "desc"] = "desc",
        sort: Literal[
            "time_created", "time_left", "current_price", "buyout_price"
        ] = "time_created",
    ) -> dict[str, Any]:
        """
        Получить активные лоты аукциона

        Args:
            region: Регион (EU, RU, NA, SEA)
            item_id: ID предмета (например, "y1q9")
            additional: Включить дополнительную информацию
            limit: Количество лотов (0-200)
            offset: Сдвиг в списке
            order: Порядок сортировки (asc/desc)
            sort: Поле для сортировки

        Returns:
            {"total": int, "lots": [...]}
        """
        url = f"{self.base_url}/{region}/auction/{item_id}/lots"

        params = {
            "additional": str(additional).lower(),
            "limit": str(limit),
            "offset": str(offset),
            "order": order,
            "sort": sort,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers=self._get_headers(),
                    params=params,
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise StalcraftAPIError(
                f"API error {e.response.status_code}: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise StalcraftAPIError(f"Request error: {str(e)}")

    async def get_auction_history(
        self,
        region: str,
        item_id: str,
        additional: bool = False,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """
        Получить историю продаж

        Args:
            region: Регион (EU, RU, NA, SEA)
            item_id: ID предмета (например, "y1q9")
            additional: Включить дополнительную информацию
            limit: Количество записей (0-200)
            offset: Сдвиг в списке

        Returns:
            {"total": int, "prices": [...]}
        """
        url = f"{self.base_url}/{region}/auction/{item_id}/history"

        params = {
            "additional": str(additional).lower(),
            "limit": str(limit),
            "offset": str(offset),
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers=self._get_headers(),
                    params=params,
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise StalcraftAPIError(
                f"API error {e.response.status_code}: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise StalcraftAPIError(f"Request error: {str(e)}")


# Singleton
stalcraft_client = StalcraftAPIClient()
