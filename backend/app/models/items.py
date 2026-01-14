from pydantic import BaseModel, Field
from typing import Optional


class ItemName(BaseModel):
    """Translatable item name"""

    type: str  # "translation" or "text"
    key: Optional[str] = None
    lines: Optional[dict[str, str]] = None  # {"ru": "название", "en": "name"}
    text: Optional[str] = None  # For type="text"


class Item(BaseModel):
    """
    Item model from stalcraft-database repository
    Based on structure from https://github.com/EXBO-Studio/stalcraft-database/
    """

    id: str = Field(..., description="Item ID")
    category: str = Field(..., description="Category (weapon/pistol)")
    name: ItemName = Field(..., description="Translatable name")
    color: Optional[str] = Field(None, description="Item color/rank")

    # Additional fields for UI
    display_name: Optional[str] = Field(None, description="Display name")
    icon_url: Optional[str] = Field(None, description="Icon URL")

    class Config:
        extra = "allow"  # Allow additional fields from JSON


class ItemSearchResult(BaseModel):
    """Search result (simplified version)"""

    id: str
    name: str
    category: str
    icon_url: Optional[str] = None


class ItemsListResponse(BaseModel):
    """Response with list of items"""

    items: list[ItemSearchResult]
    total: int = Field(default=0, description="Total number of items")
