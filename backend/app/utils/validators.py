"""
Validation utilities
"""
from app.config import settings


def validate_region(region: str) -> bool:
    """Проверить валидность региона"""
    return region.upper() in settings.SUPPORTED_REGIONS


def validate_item_id(item_id: str) -> bool:
    """
    Проверить валидность ID предмета
    
    TODO: Реализовать после изучения формата ID из stalcraft-database
    """
    return bool(item_id and len(item_id) > 0)
