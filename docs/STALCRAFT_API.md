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
- **Demo API** (`dapi.stalcraft.net`) - для тестирования с публичным токеном
- **Production API** (`eapi.stalcraft.net`) - требует личный Bearer token

**Важно:** Оба API требуют токена авторизации!

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

### Типы токенов

Stalcraft API предоставляет два типа токенов:

1. **App Access Token** - для публичных данных:
   - Аукцион (лоты, история)
   - Предметы
   - Информация о кланах
   - Статистика

2. **User Access Token** - для персональных данных:
   - Профиль пользователя
   - Персонажи
   - Личные достижения

### Demo API

Demo API использует **публичный App Access Token**:

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwibmJmIjoxNjczNzk3ODM4LCJleHAiOjQ4MjczOTc4MzgsImlhdCI6MTY3Mzc5NzgzOCwianRpIjoiYXhwbzAzenJwZWxkMHY5dDgzdzc1N2x6ajl1MmdyeHVodXVlb2xsZ3M2dml1YjVva3NwZTJ3eGFrdjJ1eWZxaDU5ZDE2ZTNlN2FqdW16Z3gifQ.ZNSsvwAX72xT5BzLqqYABuH2FGbOlfiXMK5aYO1H5llG51ZjcPvOYBDRR4HUoPZVLFY8jyFUsEXNM7SYz8qL9ePmLjJl6pib8FEtqVPmf9ldXvKkbaaaSp4KkJzsIEMY_Z5PejB2Vr-q-cL13KPgnLGUaSW-2X_sHPN7VZJNMjRgjw4mPiRZTe4CEpQq0BEcPrG6OLtU5qlZ6mLDJBjN2xtK0DI6xgmYriw_5qW1mj1nqF_ewtUiQ1KTVhDgXnaNUdkGsggAGqyicTei0td6DTKtnl3noD5VkipWn_CwSqb2Mhm16I9BPfX_d5ARzWrnrwPRUf6PA_7LipNU6KkkW0mhZfmwEPTm_sXPus0mHPENoVZArdFT3L5sOYBcpqwvVIEtxRUTdcsKp-y-gSzao5muoyPVoCc2LEeHEWx0cIi9spsZ46SPRQpN4baVFp7y5rp5pjRsBKHQYUJ0lTmh1_vyfzOzbtNN2v6W_5w9JTLrN1U6fhmifvKHppFSEqD6DameL1TC59kpIdufRkEU9HE4O-ErEf1GuJFRx-Dew6XDvb_ExhvEqcw31yNvKzpVqLYJfLazqn6tUbVuAiPwpy6rP9tYO2taT1vj5TGn_vxwDu9zoLWe796tFMPS-kmbCglxB5C9L4EbpfWNbWxYjUkTvjT2Ml9OnrB0UbYo1jI
```

Этот токен предоставлен Stalcraft для тестирования и уже включен в приложение.

**Пример запроса к Demo API:**
```bash
curl -X GET \
  'https://dapi.stalcraft.net/EU/auction/y1q9/lots?limit=20' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...' \
  -H 'Content-Type: application/json'
```

### Production API

Production API требует **личный токен** в заголовке:
```
Authorization: Bearer YOUR_TOKEN_HERE
```

Получение токена:
1. Зарегистрироваться на [stalcraft.net](https://stalcraft.net)
2. Перейти в раздел API в личном кабинете
3. Создать приложение и получить токен
4. Выбрать тип токена (App Access или User Access)

**Пример запроса к Production API:**
```bash
curl -X GET \
  'https://eapi.stalcraft.net/EU/auction/y1q9/lots?limit=20' \
  -H 'Authorization: Bearer YOUR_PERSONAL_TOKEN' \
  -H 'Content-Type: application/json'
```

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
# Demo API (работает из коробки)
USE_DEMO_API=true
STALCRAFT_DEMO_HOST=dapi.stalcraft.net
# Публичный токен уже включен в STALCRAFT_DEMO_TOKEN

# Production API
USE_DEMO_API=false
STALCRAFT_PROD_HOST=eapi.stalcraft.net
STALCRAFT_PROD_TOKEN=your_token_here
```

### Переключение в коде

```python
from app.config import settings

# Автоматически выбирает demo/prod URL
api_url = settings.api_base_url

# Автоматически выбирает нужный токен
api_token = settings.api_token
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
