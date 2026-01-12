from pydantic import BaseModel, Field
#from typing import Any


class Item(BaseModel):
    """
    Модель предмета из базы данных Stalcraft
    
    TODO: Адаптировать под структуру из stalcraft-database репозитория
    """
    id: str = Field(..., description="ID предмета")
    name: str = Field(..., description="Название предмета")
    category: str | None = Field(default=None, description="Категория")
    subcategory: str | None = Field(default=None, description="Подкатегория")
    
    class Config:
        extra = "allow"


class ItemsListResponse(BaseModel):
    """Ответ со списком предметов"""
    items: list[Item]
    total: int = Field(default=0, description="Общее количество предметов")
