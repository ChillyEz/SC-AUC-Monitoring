import httpx
from typing import Any
from app.config import settings
from app.core.exceptions import StalcraftAPIError


class StalcraftAPIClient:
    """
    Клиент для работы с Stalcraft API
    Поддерживает Demo и Production API
    """

    def __init__(self):
        self.base_url = settings.api_base_url
        self.use_demo = settings.USE_DEMO_API
        self.token = settings.STALCRAFT_API_TOKEN
        self.timeout = 10.0

    def _get_headers(self) -> dict[str, str]:
        """Заголовки - авторизация только для prod API"""
        if self.use_demo:
            return {}

        if not self.token:
            raise StalcraftAPIError("STALCRAFT_API_TOKEN required for production API")

        return {"Authorization": f"Bearer {self.token}"}

    async def get_auction_lots(self, region: str, item_id: str) -> dict[str, Any]:
        """
        Получить активные лоты аукциона

        TODO: Адаптировать под реальную структуру API после тестирования
        Endpoint: GET /{region}/auction/{item}/lots
        """
        url = f"{self.base_url}/{region}/auction/{item_id}/lots"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url, headers=self._get_headers(), timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise StalcraftAPIError(
                f"API error: {e.response.status_code} - {e.response.text}"
            )
        except httpx.RequestError as e:
            raise StalcraftAPIError(f"Request error: {str(e)}")

    async def get_auction_history(
        self, region: str, item_id: str, limit: int = 50
    ) -> dict[str, Any]:
        """
        Получить историю продаж

        TODO: Адаптировать под реальную структуру API после тестирования
        Endpoint: GET /{region}/auction/{item}/history
        """
        url = f"{self.base_url}/{region}/auction/{item_id}/history"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers=self._get_headers(),
                    params={"limit": limit} if limit else {},
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise StalcraftAPIError(
                f"API error: {e.response.status_code} - {e.response.text}"
            )
        except httpx.RequestError as e:
            raise StalcraftAPIError(f"Request error: {str(e)}")


# Singleton
stalcraft_client = StalcraftAPIClient()
