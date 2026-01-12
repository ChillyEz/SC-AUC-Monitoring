import httpx
from typing import Any, Literal
from app.config import settings
from app.core.exceptions import StalcraftAPIError


class StalcraftAPIClient:
    """
    Клиент для работы с Stalcraft API
    Поддерживает Demo, Production и Wiki API
    """

    def __init__(self):
        self.base_url = settings.api_base_url
        self.api_source = settings.API_SOURCE
        self.timeout = 10.0

    def _get_headers(self) -> dict[str, str]:
        """Заголовки с авторизацией для всех запросов"""
        headers = {"Content-Type": "application/json"}
        
        if self.api_source == "wiki":
            # Wiki API uses X-Internal-Key header
            headers["X-Internal-Key"] = settings.STALCRAFT_WIKI_API_KEY
        else:
            # Official API uses Bearer token authorization
            token = settings.api_token
            if not token:
                raise StalcraftAPIError("STALCRAFT API token is required")
            headers["Authorization"] = f"Bearer {token}"
        
        return headers

    def _build_url(self, endpoint: str, region: str, item_id: str) -> str:
        """Построить URL для запроса в зависимости от источника API"""
        if self.api_source == "wiki":
            if endpoint == "history":
                return f"{self.base_url}/slug/api/auction-history"
            else:  # available-lots
                return f"{self.base_url}/api/available-lots"
        else:
            # Official API
            return f"{self.base_url}/{region}/auction/{item_id}/{endpoint}"

    def _build_params(self, region: str, item_id: str, endpoint: str, **kwargs) -> dict:
        """Построить параметры запроса в зависимости от источника API"""
        if self.api_source == "wiki":
            # Wiki API uses region and id as query params
            return {"region": region.lower(), "id": item_id}
        else:
            # Official API uses kwargs as params
            return kwargs

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
        if self.api_source == "wiki":
            # Wiki API uses different endpoint and params
            url = self._build_url("available-lots", region, item_id)
            params = self._build_params(region, item_id, "available-lots")
        else:
            # Official API
            url = self._build_url("lots", region, item_id)
            params = self._build_params(
                region,
                item_id,
                "lots",
                additional=str(additional).lower(),
                limit=str(limit),
                offset=str(offset),
                order=order,
                sort=sort,
            )

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
        if self.api_source == "wiki":
            # Wiki API uses different endpoint and params
            url = self._build_url("history", region, item_id)
            params = self._build_params(region, item_id, "history")
        else:
            # Official API
            url = self._build_url("history", region, item_id)
            params = self._build_params(
                region,
                item_id,
                "history",
                additional=str(additional).lower(),
                limit=str(limit),
                offset=str(offset),
            )

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
