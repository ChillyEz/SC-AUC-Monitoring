"""
Auction service - бизнес-логика для работы с аукционом
"""
#from typing import Any
from app.clients.stalcraft import stalcraft_client
from app.models.auction import AuctionLotsResponse, AuctionHistoryResponse, AuctionLot, AuctionHistoryItem
from app.core.exceptions import InvalidRegionError
from app.config import settings


class AuctionService:
    """Сервис для работы с аукционом"""
    
    async def get_lots(self, region: str, item_id: str) -> AuctionLotsResponse:
        """
        Получить активные лоты аукциона
        
        TODO: Адаптировать парсинг ответа API под реальную структуру
        """
        # Валидация региона
        if region.upper() not in settings.SUPPORTED_REGIONS:
            raise InvalidRegionError(f"Region {region} not supported. Use: {', '.join(settings.SUPPORTED_REGIONS)}")
        
        # Получить данные из API
        raw_data = await stalcraft_client.get_auction_lots(region.upper(), item_id)
        
        # TODO: Адаптировать парсинг под реальную структуру ответа
        # Пример предполагаемой структуры: {"lots": [...], "total": 10}
        lots_data = raw_data.get("lots", [])
        
        # Парсинг лотов
        lots = []
        for lot_data in lots_data:
            try:
                lot = AuctionLot(**lot_data)
                lots.append(lot)
            except Exception:
                # Пропустить невалидные лоты
                continue
        
        return AuctionLotsResponse(
            item_id=item_id,
            region=region.upper(),
            lots=lots,
            total=len(lots),
            raw_data=raw_data  # Для отладки
        )
    
    async def get_history(self, region: str, item_id: str, limit: int = 50) -> AuctionHistoryResponse:
        """
        Получить историю продаж
        
        TODO: Адаптировать парсинг ответа API под реальную структуру
        """
        # Валидация региона
        if region.upper() not in settings.SUPPORTED_REGIONS:
            raise InvalidRegionError(f"Region {region} not supported. Use: {', '.join(settings.SUPPORTED_REGIONS)}")
        
        # Получить данные из API
        raw_data = await stalcraft_client.get_auction_history(region.upper(), item_id, limit)
        
        # TODO: Адаптировать парсинг под реальную структуру ответа
        # Пример предполагаемой структуры: {"history": [...], "total": 50}
        history_data = raw_data.get("history", [])
        
        # Парсинг истории
        history = []
        for item_data in history_data:
            try:
                item = AuctionHistoryItem(**item_data)
                history.append(item)
            except Exception:
                # Пропустить невалидные записи
                continue
        
        return AuctionHistoryResponse(
            item_id=item_id,
            region=region.upper(),
            history=history,
            total=len(history),
            raw_data=raw_data  # Для отладки
        )


# Singleton
auction_service = AuctionService()
