from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any

# TODO: Эти модели нужно адаптировать после получения реальных данных из API
# Сейчас это примерная структура для разработки


class AuctionLot(BaseModel):
    """
    Модель активного лота на аукционе
    
    TODO: Адаптировать поля под реальный JSON из API
    Возможные поля (примерные):
    - price: int | float
    - amount: int
    - seller: str | None
    - time_left: int | str
    - created_at: datetime
    """
    price: int = Field(..., description="Цена лота")
    amount: int = Field(default=1, description="Количество предметов")
    time_left: str | None = Field(default=None, description="Оставшееся время")
    
    # Дополнительные поля - раскомментировать после проверки API
    # seller: str | None = None
    # created_at: datetime | None = None
    
    class Config:
        extra = "allow"  # Разрешить дополнительные поля из API


class AuctionHistoryItem(BaseModel):
    """
    Модель записи из истории продаж
    
    TODO: Адаптировать поля под реальный JSON из API
    Возможные поля (примерные):
    - price: int | float
    - amount: int
    - sold_at: datetime
    - buyer: str | None
    - seller: str | None
    """
    price: int = Field(..., description="Цена продажи")
    amount: int = Field(default=1, description="Количество проданных предметов")
    sold_at: datetime | None = Field(default=None, description="Время продажи")
    
    # Дополнительные поля - раскомментировать после проверки API
    # buyer: str | None = None
    # seller: str | None = None
    
    class Config:
        extra = "allow"  # Разрешить дополнительные поля из API


class AuctionLotsResponse(BaseModel):
    """Ответ со списком активных лотов"""
    item_id: str
    region: str
    lots: list[AuctionLot]
    total: int = Field(default=0, description="Общее количество лотов")
    
    # Сырые данные для отладки
    raw_data: dict[str, Any] | None = Field(default=None, description="Сырой ответ API (для отладки)")


class AuctionHistoryResponse(BaseModel):
    """Ответ с историей продаж"""
    item_id: str
    region: str
    history: list[AuctionHistoryItem]
    total: int = Field(default=0, description="Общее количество записей")
    
    # Сырые данные для отладки
    raw_data: dict[str, Any] | None = Field(default=None, description="Сырой ответ API (для отладки)")
