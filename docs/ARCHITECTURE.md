# Architecture Documentation

Архитектура проекта SC-AUC-Monitoring

## Обзор

SC-AUC-Monitoring построен на модульной архитектуре с четким разделением ответственности между компонентами.

## Архитектурная диаграмма

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  HTML/   │  │   CSS    │  │JavaScript│  │Components│   │
│  │Templates │  │  Styles  │  │  Logic   │  │  Modules │   │
│  └────┬─────┘  └──────────┘  └─────┬────┘  └──────────┘   │
│       │                              │                      │
└───────┼──────────────────────────────┼──────────────────────┘
        │                              │
        │         HTTP / REST          │
        │                              │
┌───────┼──────────────────────────────┼──────────────────────┐
│       │        FastAPI App           │                      │
│       ▼                              ▼                      │
│  ┌─────────┐                   ┌─────────┐                 │
│  │ Static  │                   │   API   │                 │
│  │  Files  │                   │ Router  │                 │
│  └─────────┘                   └────┬────┘                 │
│                                     │                      │
│                            ┌────────┴────────┐             │
│                            │                 │             │
│                     ┌──────▼──────┐  ┌──────▼──────┐      │
│                     │   Auction   │  │    Items    │      │
│                     │  Endpoints  │  │  Endpoints  │      │
│                     └──────┬──────┘  └──────┬──────┘      │
│                            │                 │             │
│                     ┌──────▼──────┐  ┌──────▼──────┐      │
│                     │   Auction   │  │    Items    │      │
│                     │   Service   │  │   Service   │      │
│                     └──────┬──────┘  └──────┬──────┘      │
│                            │                 │             │
│                     ┌──────▼──────┐  ┌──────▼──────┐      │
│                     │ Stalcraft   │  │   GitHub    │      │
│                     │API Client   │  │    API      │      │
│                     └──────┬──────┘  └──────┬──────┘      │
└────────────────────────────┼─────────────────┼─────────────┘
                             │                 │
                             │                 │
                     ┌───────▼──────┐  ┌───────▼──────┐
                     │  Stalcraft   │  │    GitHub    │
                     │     API      │  │  stalcraft-  │
                     │ (Demo/Prod)  │  │  database    │
                     └──────────────┘  └──────────────┘
```

## Компоненты

### Backend (FastAPI)

#### 1. API Layer (`app/api/`)
- **Роль**: Обработка HTTP запросов, валидация входных данных
- **Компоненты**:
  - `v1/router.py` - главный роутер API v1
  - `v1/auction.py` - endpoints для аукциона
  - `v1/items.py` - endpoints для предметов

#### 2. Services Layer (`app/services/`)
- **Роль**: Бизнес-логика приложения
- **Компоненты**:
  - `auction_service.py` - логика работы с аукционом
  - `items_service.py` - логика работы с предметами
- **Особенности**:
  - Отделяет бизнес-логику от API endpoints
  - Обрабатывает данные перед отправкой клиенту
  - Готово к расширению (кэширование, аналитика)

#### 3. Clients Layer (`app/clients/`)
- **Роль**: Взаимодействие с внешними API
- **Компоненты**:
  - `base.py` - базовый HTTP клиент
  - `stalcraft.py` - клиент Stalcraft API
- **Особенности**:
  - Инкапсулирует логику HTTP запросов
  - Поддержка Demo и Production API
  - Обработка ошибок внешних API

#### 4. Models Layer (`app/models/`)
- **Роль**: Pydantic модели для доменных объектов
- **Компоненты**:
  - `auction.py` - модели аукциона (лоты, история)
  - `items.py` - модели предметов
- **Особенности**:
  - Гибкие модели с `extra = "allow"`
  - TODO комментарии для адаптации
  - Поле `raw_data` для отладки

#### 5. Schemas Layer (`app/schemas/`)
- **Роль**: Request/Response схемы для API
- **Компоненты**:
  - `requests.py` - схемы запросов
  - `responses.py` - схемы ответов
- **Особенности**:
  - Валидация входных данных
  - Документация API

#### 6. Core Layer (`app/core/`)
- **Роль**: Ядро приложения
- **Компоненты**:
  - `exceptions.py` - кастомные исключения
  - `dependencies.py` - FastAPI dependencies
- **Особенности**:
  - Централизованная обработка ошибок
  - Переиспользуемые зависимости

#### 7. Utils Layer (`app/utils/`)
- **Роль**: Утилитарные функции
- **Компоненты**:
  - `validators.py` - валидаторы
- **Особенности**:
  - Переиспользуемые helper функции

#### 8. Configuration (`app/config.py`)
- **Роль**: Конфигурация приложения
- **Особенности**:
  - Pydantic Settings
  - Environment variables
  - Demo/Production переключение

### Frontend (HTML/CSS/JS)

#### 1. Templates (`frontend/templates/`)
- `index.html` - главная страница
- Простая структура для MVP

#### 2. Static Files (`frontend/static/`)
- **CSS**:
  - `main.css` - основные стили
  - `components/*.css` - компоненты стили
- **JavaScript**:
  - `api.js` - API клиент
  - `main.js` - главная логика
  - `components/*.js` - UI компоненты

## Принципы проектирования

### 1. Separation of Concerns
Каждый слой имеет четкую ответственность:
- API → Обработка запросов
- Services → Бизнес-логика
- Clients → Внешние API
- Models → Структуры данных

### 2. Modularity
Модули независимы и легко заменяемы:
- Можно заменить Stalcraft клиент
- Можно добавить новые services
- Можно расширить API версии

### 3. Flexibility
Готовность к изменениям:
- Гибкие модели данных
- TODO комментарии
- `extra = "allow"` для неизвестных полей

### 4. Extensibility
Готовность к расширению:
- Структура для новых endpoints
- Место для кэширования
- Место для БД (Этап 2)

## Потоки данных

### Получение лотов аукциона

```
User → Frontend → API Endpoint → Service → Client → Stalcraft API
                                                           │
                                                           ▼
User ← Frontend ← API Endpoint ← Service ← Client ← Response
```

1. Пользователь вводит region и item_id
2. Frontend вызывает `/api/v1/auction/{region}/{item_id}/lots`
3. Auction endpoint валидирует параметры
4. AuctionService обрабатывает запрос
5. StalcraftAPIClient делает HTTP запрос к Stalcraft API
6. Ответ парсится в AuctionLotsResponse
7. JSON возвращается пользователю

## Безопасность

### Текущая реализация (MVP)
- CORS настроен для localhost
- Валидация входных данных (Pydantic)
- Обработка исключений

### Будущие улучшения (Этапы 2-4)
- Rate limiting
- API key authentication
- SQL injection защита (с БД)
- XSS защита

## Масштабирование

### Текущая архитектура (MVP)
- Один процесс FastAPI
- In-memory данные
- Синхронные запросы к API

### Готовность к масштабированию
- Async/await для IO операций
- Stateless архитектура
- Готово к Redis кэшу
- Готово к PostgreSQL

### Этап 2: База данных
```
Backend → PostgreSQL
       ← Исторические данные
```

### Этап 3: Мониторинг
```
Scheduler → Background Tasks → Notifications
```

## Технологический стек

### Backend
- **Framework**: FastAPI 0.109.1
- **Server**: Uvicorn
- **Validation**: Pydantic 2.5.0
- **HTTP Client**: httpx 0.25.2
- **Python**: 3.11+

### Frontend
- **HTML5**
- **CSS3** (Custom, no frameworks)
- **Vanilla JavaScript** (ES6+)

### DevOps
- **Docker** (для деплоя)
- **Git** (version control)

### Планируется (Этап 2)
- **PostgreSQL** (база данных)
- **Redis** (кэш)
- **Celery** (background tasks)

## Паттерны

### 1. Repository Pattern
- Services → Clients → External APIs
- Отделяет бизнес-логику от data access

### 2. Singleton Pattern
- API clients (stalcraft_client)
- Services (auction_service, items_service)
- Configuration (settings)

### 3. Dependency Injection
- FastAPI dependencies
- Готовность к тестированию

## Тестирование

### Структура тестов
```
tests/
├── conftest.py           # Fixtures
├── test_api/             # API tests
├── test_services/        # Service tests
└── test_clients/         # Client tests
```

### Стратегия
- Unit tests для services
- Integration tests для API
- Mocks для external APIs

---

**Version**: 0.1.0  
**Last Updated**: 2026-01-11
