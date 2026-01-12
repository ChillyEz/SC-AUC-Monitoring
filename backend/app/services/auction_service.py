"""
Auction service - бизнес-логика для работы с аукционом
"""

from typing import Literal
from app.clients.stalcraft import stalcraft_client
from app.models.auction import AuctionLotsResponse, AuctionHistoryResponse
from app.core.exceptions import InvalidRegionError
from app.config import settings


class AuctionService:
    """Сервис для работы с аукционом"""

    def __init__(self):
        self.client = stalcraft_client

    def _validate_region(self, region: str) -> None:
        """Проверить валидность региона"""
        if region.upper() not in settings.SUPPORTED_REGIONS:
            raise InvalidRegionError(
                f"Invalid region '{region}'. "
                f"Supported: {', '.join(settings.SUPPORTED_REGIONS)}"
            )

    async def get_lots(
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
    ) -> AuctionLotsResponse:
        """Получить активные лоты"""
        self._validate_region(region)

        data = await self.client.get_auction_lots(
            region=region.upper(),
            item_id=item_id,
            additional=additional,
            limit=limit,
            offset=offset,
            order=order,
            sort=sort,
        )

        return AuctionLotsResponse(**data)

    async def get_history(
        self,
        region: str,
        item_id: str,
        additional: bool = False,
        limit: int = 20,
        offset: int = 0,
    ) -> AuctionHistoryResponse:
        """Получить историю продаж"""
        self._validate_region(region)

        data = await self.client.get_auction_history(
            region=region.upper(),
            item_id=item_id,
            additional=additional,
            limit=limit,
            offset=offset,
        )

        return AuctionHistoryResponse(**data)


# Singleton
auction_service = AuctionService()
