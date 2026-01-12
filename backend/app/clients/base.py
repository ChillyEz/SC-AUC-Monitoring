"""
Base HTTP client utilities
"""

import httpx
from typing import Any


class BaseHTTPClient:
    """
    Базовый HTTP клиент с общими методами
    """

    def __init__(self, base_url: str, timeout: float = 10.0):
        self.base_url = base_url
        self.timeout = timeout

    async def get(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Базовый GET запрос"""
        url = f"{self.base_url}{endpoint}"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url, headers=headers or {}, params=params or {}, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
