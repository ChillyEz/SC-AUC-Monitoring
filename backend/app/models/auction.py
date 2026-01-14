from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any, Literal, Optional


# Типы для параметров запроса
AuctionSortField = Literal["time_created", "time_left", "current_price", "buyout_price"]
SortOrder = Literal["asc", "desc"]


class AuctionLot(BaseModel):
    """
    Активный лот на аукционе

    Структура из реального API Stalcraft
    """

    itemId: str = Field(..., description="ID предмета")
    amount: int = Field(..., description="Количество предметов в лоте")
    startPrice: int = Field(..., description="Начальная цена")
    # Сделать опциональным, т.к. Demo API может не возвращать это поле
    currentPrice: Optional[int] = Field(None, description="Текущая цена")
    buyoutPrice: int = Field(..., description="Цена немедленного выкупа")
    startTime: datetime = Field(..., description="Время создания лота")
    endTime: datetime = Field(..., description="Время окончания лота")
    additional: dict[str, Any] = Field(
        default_factory=dict, description="Дополнительная информация (если запрошена)"
    )

    class Config:
        # Разрешить дополнительные поля, которые не описаны в модели
        extra = "ignore"

        json_schema_extra = {
            "example": {
                "itemId": "y1q9",
                "amount": 5,
                "startPrice": 10000,
                "currentPrice": 12000,
                "buyoutPrice": 15000,
                "startTime": "2026-01-12T10:00:00Z",
                "endTime": "2026-01-13T10:00:00Z",
                "additional": {},
            }
        }


class AuctionLotsResponse(BaseModel):
    """Ответ API со списком активных лотов"""

    total: int = Field(
        ..., description="Общее количество лотов в базе (не только в ответе)"
    )
    lots: list[AuctionLot] = Field(default_factory=list, description="Список лотов")


class AuctionPriceHistory(BaseModel):
    """
    Запись из истории продаж

    Структура из реального API Stalcraft
    """

    amount: int = Field(..., description="Количество проданных предметов")
    price: int = Field(..., description="Цена продажи")
    time: datetime = Field(..., description="Время продажи (UTC)")
    additional: dict[str, Any] = Field(
        default_factory=dict, description="Дополнительная информация (если запрошена)"
    )

    class Config:
        # Разрешить дополнительные поля, которые не описаны в модели
        extra = "ignore"

        json_schema_extra = {
            "example": {
                "amount": 3,
                "price": 14500,
                "time": "2026-01-12T14:30:00Z",
                "additional": {},
            }
        }


class AuctionHistoryResponse(BaseModel):
    """Ответ API с историей продаж"""

    total: int = Field(..., description="Общее количество записей в базе")
    prices: list[AuctionPriceHistory] = Field(
        default_factory=list, description="История цен (отсортирована по времени)"
    )
