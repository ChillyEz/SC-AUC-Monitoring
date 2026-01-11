# Stalcraft API Documentation

Документация по Stalcraft API для SC-AUC-Monitoring

## Обзор

Stalcraft предоставляет два API:
- **Demo API** (`dapi.stalcraft.net`) - для тестирования, без авторизации
- **Production API** (`eapi.stalcraft.net`) - требует Bearer token

## API Endpoints

### Base URLs

```
Demo:       https://dapi.stalcraft.net
Production: https://eapi.stalcraft.net
```

### Формат endpoints

```
https://{host}/{region}/auction/{item_id}/{endpoint}
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

## Auction Endpoints

### 1. Get Auction Lots

Получить активные лоты аукциона для предмета.

**Endpoint:**
```
GET /{region}/auction/{item_id}/lots
```

**Parameters:**
- `region` (path) - Регион (EU, RU, NA, SEA)
- `item_id` (path) - ID предмета из stalcraft-database

**Example Request:**
```bash
# Demo API
curl https://dapi.stalcraft.net/EU/auction/weapon_rifle_ak47/lots

# Production API
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://eapi.stalcraft.net/EU/auction/weapon_rifle_ak47/lots
```

**Expected Response Structure:**
```json
{
  "lots": [
    {
      "price": 5000,
      "amount": 1,
      "time_left": "2h 30m",
      "seller": "player_name",
      "created_at": "2026-01-11T12:00:00Z"
    }
  ],
  "total": 1
}
```

⚠️ **TODO**: Структура ответа примерная. Необходимо проверить с реальным API.

### 2. Get Auction History

Получить историю продаж предмета.

**Endpoint:**
```
GET /{region}/auction/{item_id}/history
```

**Parameters:**
- `region` (path) - Регион (EU, RU, NA, SEA)
- `item_id` (path) - ID предмета
- `limit` (query, optional) - Количество записей (default: 50)

**Example Request:**
```bash
# Demo API
curl "https://dapi.stalcraft.net/EU/auction/weapon_rifle_ak47/history?limit=20"

# Production API
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://eapi.stalcraft.net/EU/auction/weapon_rifle_ak47/history?limit=20"
```

**Expected Response Structure:**
```json
{
  "history": [
    {
      "price": 4800,
      "amount": 1,
      "sold_at": "2026-01-11T10:30:00Z",
      "buyer": "player_name",
      "seller": "another_player"
    }
  ],
  "total": 1
}
```

⚠️ **TODO**: Структура ответа примерная. Необходимо проверить с реальным API.

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

### Item JSON Structure

⚠️ **TODO**: Изучить реальную структуру JSON из репозитория.

Предполагаемая структура:
```json
{
  "id": "weapon_rifle_ak47",
  "name": "AK-47",
  "name_ru": "АК-47",
  "description": "Assault rifle",
  "category": "weapons",
  "subcategory": "rifles",
  "rarity": "rare",
  "stats": {
    "damage": 45,
    "accuracy": 70,
    "range": 80
  }
}
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
ITEM_ID = "real_item_id"  # Реальный ID предмета
```

### Результаты

Скрипт создаст файлы:
- `docs/auction_lots_example_EU_item_id.json`
- `docs/auction_history_example_EU_item_id.json`

Используйте эти файлы для:
1. Изучения реальной структуры API
2. Адаптации моделей в `app/models/auction.py`
3. Обновления парсинга в `app/services/auction_service.py`

## Адаптация кода под реальный API

### Шаг 1: Получить реальные данные

```bash
python scripts/test_api.py
```

### Шаг 2: Изучить структуру

Откройте `docs/auction_lots_example_*.json` и изучите поля.

### Шаг 3: Обновить модели

В `app/models/auction.py`:
```python
class AuctionLot(BaseModel):
    # Раскомментируйте и добавьте реальные поля
    price: int
    amount: int
    time_left: str | None = None
    seller: str | None = None  # Раскомментировать если есть в API
    created_at: datetime | None = None  # Раскомментировать если есть в API
```

### Шаг 4: Обновить парсинг

В `app/services/auction_service.py`:
```python
async def get_lots(self, region: str, item_id: str):
    raw_data = await stalcraft_client.get_auction_lots(region, item_id)
    
    # Адаптировать под реальную структуру
    lots_data = raw_data.get("lots", [])  # Или другой ключ
    
    # Парсинг
    lots = [AuctionLot(**lot_data) for lot_data in lots_data]
```

## Rate Limits

⚠️ **TODO**: Узнать ограничения rate limits из официальной документации.

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

## Официальная документация

⚠️ **TODO**: Добавить ссылки на официальную Stalcraft API документацию когда будет доступна.

Проверьте:
- Официальный сайт Stalcraft
- Discord сообщество
- GitHub репозитории

## Примеры использования

### Python (httpx)

```python
import httpx

async def get_auction_data(region, item_id):
    url = f"https://dapi.stalcraft.net/{region}/auction/{item_id}/lots"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10.0)
        return response.json()
```

### cURL

```bash
# Get lots
curl "https://dapi.stalcraft.net/EU/auction/item_id/lots"

# Get history with limit
curl "https://dapi.stalcraft.net/EU/auction/item_id/history?limit=20"
```

### JavaScript (fetch)

```javascript
async function getAuctionLots(region, itemId) {
    const url = `https://dapi.stalcraft.net/${region}/auction/${itemId}/lots`;
    const response = await fetch(url);
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

**Version**: 0.1.0  
**Last Updated**: 2026-01-11

⚠️ **Важно**: Эта документация основана на предположениях. После получения реального доступа к API необходимо обновить все примеры и структуры данных.
