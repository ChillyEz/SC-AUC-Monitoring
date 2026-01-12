# Stalcraft API - Аукцион

## Endpoints

### 1. Получение активных лотов

**Endpoint:** `GET /{region}/auction/{item}/lots`

**URL:** `https://eapi.stalcraft.net/{region}/auction/{item}/lots`

**Path параметры:**
- `region` (string, required) - Регион: EU, RU, NA, SEA
- `item` (string, required) - ID предмета (например, "y1q9")

**Query параметры:**
- `additional` (string) - "true" или "false", по умолчанию "false"
- `limit` (string) - Количество лотов (0-200), по умолчанию 20
- `offset` (string) - Сдвиг в списке, по умолчанию 0
- `order` (string) - "asc" или "desc"
- `sort` (string) - "time_created", "time_left", "current_price", "buyout_price"

**Структура ответа:**
```json
{
  "total": 150,
  "lots": [
    {
      "itemId": "y1q9",
      "amount": 5,
      "startPrice": 10000,
      "currentPrice": 12000,
      "buyoutPrice": 15000,
      "startTime": "2026-01-12T10:00:00Z",
      "endTime": "2026-01-13T10:00:00Z",
      "additional": {}
    }
  ]
}
```

### 2. Получение истории цен

**Endpoint:** `GET /{region}/auction/{item}/history`

**URL:** `https://eapi.stalcraft.net/{region}/auction/{item}/history`

**Path параметры:**
- `region` (string, required) - Регион: EU, RU, NA, SEA
- `item` (string, required) - ID предмета

**Query параметры:**
- `additional` (string) - "true" или "false", по умолчанию "false"
- `limit` (string) - Количество записей (0-200), по умолчанию 20
- `offset` (string) - Сдвиг в списке, по умолчанию 0

**Структура ответа:**
```json
{
  "total": 500,
  "prices": [
    {
      "amount": 3,
      "price": 14500,
      "time": "2026-01-12T14:30:00Z",
      "additional": {}
    }
  ]
}
```

## Примеры использования

### Python (httpx)
```python
import httpx

async def get_lots():
    url = "https://eapi.stalcraft.net/EU/auction/y1q9/lots"
    headers = {"Authorization": "Bearer YOUR_TOKEN"}
    params = {"limit": 50, "sort": "current_price", "order": "asc"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        return response.json()
```

### Curl
```bash
curl -X GET \
  'https://eapi.stalcraft.net/EU/auction/y1q9/lots?limit=50&sort=current_price&order=asc' \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json'
```

## Обзор

Stalcraft предоставляет два API:
- **Demo API** (`dapi.stalcraft.net`) - для тестирования, без авторизации
- **Production API** (`eapi.stalcraft.net`) - требует Bearer token

## API Base URLs

```
Demo:       https://dapi.stalcraft.net
Production: https://eapi.stalcraft.net
```

## Регионы

Доступные регионы:
- **EU** - Europe
- **RU** - Russia
- **NA** - North America
- **SEA** - Southeast Asia

## Авторизация

### Demo API
Авторизация **не требуется**.

### Production API
Требуется Bearer token в заголовке:
```
Authorization: Bearer YOUR_TOKEN_HERE
```

Получение токена:
1. Зарегистрироваться на официальном сайте Stalcraft
2. Получить API token в личном кабинете
3. Использовать в заголовке запросов

## Items Database

### GitHub Repository

Stalcraft предоставляет базу предметов в отдельном репозитории:

**Repository:** https://github.com/EXBO-Studio/stalcraft-database

### Структура

```
stalcraft-database/
├── global/                    # Global realm
│   ├── items/
│   │   ├── weapons/
│   │   │   ├── rifles/
│   │   │   │   └── ak47.json
│   │   │   └── pistols/
│   │   ├── armor/
│   │   └── consumables/
│   └── icons/
│       ├── weapons/
│       │   ├── rifles/
│       │   │   └── ak47.png
│       │   └── pistols/
│       └── armor/
└── ru/                        # Russian realm
    ├── items/
    └── icons/
```

### Получение данных предмета

**URL формат:**
```
https://raw.githubusercontent.com/EXBO-Studio/stalcraft-database/main/{realm}/items/{category}/{subcategory}/{item_id}.json
```

**Пример:**
```
https://raw.githubusercontent.com/EXBO-Studio/stalcraft-database/main/global/items/weapons/rifles/ak47.json
```

### Получение иконки

**URL формат:**
```
https://raw.githubusercontent.com/EXBO-Studio/stalcraft-database/main/{realm}/icons/{category}/{subcategory}/{item_id}.png
```

**Пример:**
```
https://raw.githubusercontent.com/EXBO-Studio/stalcraft-database/main/global/icons/weapons/rifles/ak47.png
```

## Тестирование API

### Скрипт test_api.py

Используйте предоставленный скрипт для тестирования:

```bash
python scripts/test_api.py
```

Скрипт:
1. Делает запросы к Stalcraft API
2. Выводит JSON ответы
3. Сохраняет примеры в `docs/`

### Настройка скрипта

Отредактируйте переменные:
```python
REGION = "EU"  # Ваш регион
ITEM_ID = "y1q9"  # Реальный ID предмета
```

### Результаты

Скрипт создаст файлы:
- `docs/auction_lots_example_EU_item_id.json`
- `docs/auction_history_example_EU_item_id.json`

## Rate Limits

Рекомендации:
- Кэшировать запросы
- Использовать разумные интервалы обновления
- Обрабатывать 429 (Too Many Requests)

## Обработка ошибок

### Возможные ошибки

- **400** - Bad Request (invalid parameters)
- **401** - Unauthorized (invalid/missing token)
- **404** - Not Found (item doesn't exist)
- **429** - Too Many Requests (rate limit)
- **500** - Internal Server Error
- **502** - Bad Gateway
- **503** - Service Unavailable

### Обработка в коде

```python
try:
    data = await stalcraft_client.get_auction_lots(region, item_id)
except httpx.HTTPStatusError as e:
    if e.response.status_code == 404:
        raise ItemNotFoundError("Item not found")
    elif e.response.status_code == 429:
        # Implement retry logic
        pass
    else:
        raise StalcraftAPIError(f"API error: {e}")
```

## Best Practices

1. **Кэширование**: Кэшируйте данные предметов (они редко меняются)
2. **Rate Limiting**: Уважайте лимиты API
3. **Error Handling**: Обрабатывайте все возможные ошибки
4. **Logging**: Логируйте запросы для отладки
5. **Timeouts**: Используйте разумные timeout'ы (10-30 сек)

## Конфигурация в приложении

### .env настройки

```env
# Demo API (тестирование)
USE_DEMO_API=true
STALCRAFT_DEMO_HOST=dapi.stalcraft.net

# Production API
USE_DEMO_API=false
STALCRAFT_PROD_HOST=eapi.stalcraft.net
STALCRAFT_API_TOKEN=your_token_here
```

### Переключение в коде

```python
from app.config import settings

# Автоматически выбирает demo/prod
api_url = settings.api_base_url
```

## Примеры использования (JavaScript)

### JavaScript (fetch)

```javascript
async function getAuctionLots(region, itemId) {
    const url = `https://eapi.stalcraft.net/${region}/auction/${itemId}/lots`;
    const params = new URLSearchParams({
        limit: '50',
        sort: 'current_price',
        order: 'asc'
    });
    
    const response = await fetch(`${url}?${params}`, {
        headers: {
            'Authorization': 'Bearer YOUR_TOKEN',
            'Content-Type': 'application/json'
        }
    });
    
    return await response.json();
}
```

## Поддержка

При проблемах с API:
1. Проверьте формат запроса
2. Проверьте валидность item_id
3. Проверьте token (для prod API)
4. Проверьте логи запросов
5. Обратитесь в поддержку Stalcraft

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-12

✅ **Документация обновлена**: Эта документация основана на официальной структуре Stalcraft API.
