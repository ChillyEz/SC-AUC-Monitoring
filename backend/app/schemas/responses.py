"""
Response schemas for API endpoints
"""

from pydantic import BaseModel, Field

# from typing import Any


class ErrorResponse(BaseModel):
    """Стандартный ответ с ошибкой"""

    error: str = Field(..., description="Описание ошибки")
    detail: str | None = Field(default=None, description="Детали ошибки")


class SuccessResponse(BaseModel):
    """Стандартный ответ об успехе"""

    success: bool = Field(default=True, description="Статус операции")
    message: str | None = Field(default=None, description="Сообщение")
