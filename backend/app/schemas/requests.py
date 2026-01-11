"""
Request schemas for API endpoints
"""
from pydantic import BaseModel, Field


class AuctionLotsRequest(BaseModel):
    """Запрос активных лотов"""
    region: str = Field(..., description="Регион (EU, RU, NA, SEA)")
    item_id: str = Field(..., description="ID предмета")


class AuctionHistoryRequest(BaseModel):
    """Запрос истории продаж"""
    region: str = Field(..., description="Регион (EU, RU, NA, SEA)")
    item_id: str = Field(..., description="ID предмета")
    limit: int = Field(default=50, description="Количество записей", ge=1, le=100)


class ItemSearchRequest(BaseModel):
    """Запрос поиска предметов"""
    query: str = Field(..., description="Поисковый запрос", min_length=1)
    realm: str = Field(default="global", description="Realm (global, ru)")
