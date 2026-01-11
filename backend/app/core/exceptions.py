class SCAUCException(Exception):
    """Базовое исключение приложения"""
    pass


class StalcraftAPIError(SCAUCException):
    """Ошибка при работе с Stalcraft API"""
    pass


class ItemNotFoundError(SCAUCException):
    """Предмет не найден"""
    pass


class InvalidRegionError(SCAUCException):
    """Невалидный регион"""
    pass
