# API Documentation

REST API документация для SC-AUC-Monitoring

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

- **Demo API**: Авторизация не требуется
- **Production API**: Bearer token в заголовке (настраивается в backend)

## Endpoints

### Health Check

#### GET `/health`

Проверка статуса API

**Response:**
```json
{
  "status": "ok",
  "version": "0.1.0",
  "environment": "development",
  "using_demo_api": true
}
```

### API Root

#### GET `/api/v1/`

Информация об API v1

**Response:**
```json
{
  "message": "SC-AUC-Monitoring API v1",
  "endpoints": {
    "auction": "/auction",
    "items": "/items",
    "docs": "/api/docs"
  }
}
```

## Auction Endpoints

### Get Auction Lots

#### GET `/api/v1/auction/{region}/{item_id}/lots`

Получить активные лоты аукциона для предмета

**Path Parameters:**
- `region` (string, required): Регион (EU, RU, NA, SEA)
- `item_id` (string, required): ID предмета

**Example Request:**
```bash
curl http://localhost:8000/api/v1/auction/EU/weapon_rifle_01/lots
```

**Response 200:**
```json
{
  "item_id": "weapon_rifle_01",
  "region": "EU",
  "lots": [
    {
      "price": 5000,
      "amount": 1,
      "time_left": "2h 30m"
    }
  ],
  "total": 1,
  "raw_data": {...}
}
```

**Response 400 (Invalid Region):**
```json
{
  "detail": "Region XX not supported. Use: EU, RU, NA, SEA"
}
```

**Response 502 (API Error):**
```json
{
  "detail": "Stalcraft API error: ..."
}
```

### Get Auction History

#### GET `/api/v1/auction/{region}/{item_id}/history`

Получить историю продаж предмета

**Path Parameters:**
- `region` (string, required): Регион (EU, RU, NA, SEA)
- `item_id` (string, required): ID предмета

**Query Parameters:**
- `limit` (integer, optional): Количество записей (1-100, default: 50)

**Example Request:**
```bash
curl http://localhost:8000/api/v1/auction/EU/weapon_rifle_01/history?limit=20
```

**Response 200:**
```json
{
  "item_id": "weapon_rifle_01",
  "region": "EU",
  "history": [
    {
      "price": 4800,
      "amount": 1,
      "sold_at": "2026-01-11T12:30:00Z"
    }
  ],
  "total": 1,
  "raw_data": {...}
}
```

## Items Endpoints

### Search Items

#### GET `/api/v1/items/search`

Поиск предметов по названию

**Query Parameters:**
- `query` (string, required): Поисковый запрос (min: 1 символ)
- `realm` (string, optional): Realm (global или ru, default: global)

**Example Request:**
```bash
curl http://localhost:8000/api/v1/items/search?query=rifle&realm=global
```

**Response 200:**
```json
{
  "items": [
    {
      "id": "weapon_rifle_01",
      "name": "Assault Rifle",
      "category": "weapons",
      "subcategory": "rifles"
    }
  ],
  "total": 1
}
```

### List Items

#### GET `/api/v1/items/list`

Получить список предметов

**Query Parameters:**
- `category` (string, optional): Фильтр по категории
- `realm` (string, optional): Realm (global или ru, default: global)

**Example Request:**
```bash
curl http://localhost:8000/api/v1/items/list?category=weapons&realm=global
```

**Response 200:**
```json
{
  "items": [],
  "total": 0
}
```

### Get Item

#### GET `/api/v1/items/{item_id}`

Получить информацию о предмете

**Path Parameters:**
- `item_id` (string, required): ID предмета

**Query Parameters:**
- `realm` (string, optional): Realm (global или ru, default: global)

**Example Request:**
```bash
curl http://localhost:8000/api/v1/items/weapon_rifle_01?realm=global
```

**Response 200:**
```json
{
  "id": "weapon_rifle_01",
  "name": "Item weapon_rifle_01",
  "category": "unknown",
  "subcategory": "unknown"
}
```

**Response 404:**
```json
{
  "detail": "Item not found"
}
```

## Error Responses

### Standard Error Format

```json
{
  "detail": "Error message"
}
```

### HTTP Status Codes

- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Not Found
- `500` - Internal Server Error
- `502` - Bad Gateway (external API error)

## Data Models

### AuctionLot

```typescript
{
  price: number,           // Цена лота
  amount: number,          // Количество (default: 1)
  time_left?: string,      // Оставшееся время
  // + additional fields from API
}
```

### AuctionHistoryItem

```typescript
{
  price: number,           // Цена продажи
  amount: number,          // Количество (default: 1)
  sold_at?: string,        // Дата продажи (ISO 8601)
  // + additional fields from API
}
```

### Item

```typescript
{
  id: string,              // ID предмета
  name: string,            // Название
  category?: string,       // Категория
  subcategory?: string,    // Подкатегория
  // + additional fields from database
}
```

## Interactive Documentation

FastAPI предоставляет интерактивную документацию:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## Notes

⚠️ **Важно**: Модели данных (AuctionLot, AuctionHistoryItem) содержат поле `extra = "allow"`, что позволяет получать дополнительные поля из Stalcraft API. После получения реальных данных необходимо адаптировать модели.

⚠️ **TODO**: Items endpoints содержат заглушки и требуют реализации после изучения структуры `stalcraft-database` репозитория.

---

**Version**: 0.1.0  
**Last Updated**: 2026-01-11
