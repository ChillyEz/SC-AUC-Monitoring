# Stage 1 MVP - Implementation Plan

План реализации Этапа 1 (MVP) для SC-AUC-Monitoring

## Цель Этапа 1

Создать базовую платформу для просмотра аукциона Stalcraft:
- ✅ Выбор региона (EU/RU/NA/SEA)
- ✅ Ввод ID предмета
- ✅ Просмотр активных лотов
- ✅ Просмотр истории продаж
- ✅ Гибкая архитектура для адаптации под реальный API

## Технический стек

### Backend
- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn 0.24.0
- **Validation**: Pydantic 2.5.0
- **HTTP Client**: httpx 0.25.2
- **Python**: 3.11+

### Frontend
- **HTML5** - структура
- **CSS3** - стили (без фреймворков)
- **JavaScript** - логика (Vanilla JS, ES6+)

### DevOps
- **Docker** - контейнеризация
- **Git** - version control

## Структура проекта

```
SC-AUC-Monitoring/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # API endpoints
│   │   ├── clients/         # External API clients
│   │   ├── models/          # Pydantic models (гибкие!)
│   │   ├── schemas/         # Request/Response schemas
│   │   ├── services/        # Business logic
│   │   ├── core/            # Core utilities
│   │   └── utils/           # Helper functions
│   ├── tests/               # Tests
│   └── requirements.txt
├── frontend/
│   ├── static/              # CSS, JS, assets
│   └── templates/           # HTML
├── docker/                  # Docker configuration
├── docs/                    # Documentation
└── scripts/                 # Utility scripts
```

## Чеклист реализации

### ✅ Backend Core
- [x] Создать структуру проекта
- [x] Настроить FastAPI приложение (`main.py`)
- [x] Настроить конфигурацию (`config.py`)
- [x] Создать кастомные исключения (`core/exceptions.py`)
- [x] Настроить CORS middleware
- [x] Создать health endpoint

### ✅ API Layer
- [x] Создать API v1 структуру
- [x] Создать главный роутер (`api/v1/router.py`)
- [x] Реализовать auction endpoints (`api/v1/auction.py`)
  - [x] GET `/{region}/{item_id}/lots`
  - [x] GET `/{region}/{item_id}/history`
- [x] Реализовать items endpoints (`api/v1/items.py`)
  - [x] GET `/search`
  - [x] GET `/list`
  - [x] GET `/{item_id}`

### ✅ Models & Schemas
- [x] Создать гибкие модели аукциона (`models/auction.py`)
  - [x] AuctionLot с `extra = "allow"`
  - [x] AuctionHistoryItem с `extra = "allow"`
  - [x] TODO комментарии для адаптации
  - [x] Поле `raw_data` для отладки
- [x] Создать модели предметов (`models/items.py`)
- [x] Создать request schemas (`schemas/requests.py`)
- [x] Создать response schemas (`schemas/responses.py`)

### ✅ Services Layer
- [x] Реализовать auction service (`services/auction_service.py`)
  - [x] Метод get_lots()
  - [x] Метод get_history()
  - [x] Валидация регионов
  - [x] Обработка ошибок
  - [x] TODO комментарии для парсинга
- [x] Реализовать items service (`services/items_service.py`)
  - [x] Заглушки методов (TODO для Этапа 1.5)

### ✅ Clients Layer
- [x] Создать базовый HTTP клиент (`clients/base.py`)
- [x] Реализовать Stalcraft API клиент (`clients/stalcraft.py`)
  - [x] Demo/Prod API переключение
  - [x] Метод get_auction_lots()
  - [x] Метод get_auction_history()
  - [x] Авторизация для prod API
  - [x] Обработка ошибок
  - [x] TODO комментарии

### ✅ Frontend
- [x] Создать главную страницу (`templates/index.html`)
  - [x] Region selector
  - [x] Item ID input
  - [x] Search button
  - [x] Lots section
  - [x] History section
  - [x] API status indicator
- [x] Создать стили (`static/css/`)
  - [x] main.css - основные стили
  - [x] auction-table.css - таблицы
  - [x] item-selector.css - селекторы
- [x] Реализовать JavaScript (`static/js/`)
  - [x] api.js - API client
  - [x] main.js - главная логика
  - [x] region-selector.js - компонент региона
  - [x] item-selector.js - компонент предмета
  - [x] auction-table.js - компонент таблиц

### ✅ Configuration
- [x] Создать requirements.txt
- [x] Создать requirements-dev.txt
- [x] Создать .env.example
- [x] Создать .gitignore
- [x] Настроить переменные окружения

### ✅ Docker
- [x] Создать Dockerfile.backend
- [x] Создать docker-compose.yml (dev)
- [x] Создать docker-compose.prod.yml (prod)

### ✅ Scripts
- [x] Создать test_api.py - тестирование Stalcraft API
- [x] Создать run_dev.sh - запуск dev сервера
- [x] Создать download_items_db.sh - скачивание базы предметов

### ✅ Documentation
- [x] Создать README.md
- [x] Создать docs/README.md
- [x] Создать docs/API.md
- [x] Создать docs/ARCHITECTURE.md
- [x] Создать docs/DEVELOPMENT.md
- [x] Создать docs/DEPLOYMENT.md
- [x] Создать docs/STALCRAFT_API.md
- [x] Создать docs/STAGE_1_MVP.md

### ✅ Testing
- [x] Создать tests структуру
- [x] Создать conftest.py с базовыми fixtures
- [x] Подготовить место для unit tests

## Ключевые особенности реализации

### 1. Гибкость моделей данных

**Проблема**: Структура Stalcraft API неизвестна заранее.

**Решение**:
```python
class AuctionLot(BaseModel):
    # Минимальные поля
    price: int
    amount: int = 1
    
    # Опциональные поля с комментариями
    # seller: str | None = None  # Раскомментировать после проверки
    
    class Config:
        extra = "allow"  # Разрешить дополнительные поля
```

### 2. Отладочные данные

**Решение**: Поле `raw_data` для просмотра оригинального ответа API:
```python
class AuctionLotsResponse(BaseModel):
    lots: list[AuctionLot]
    raw_data: dict[str, Any] | None = None  # Для отладки
```

### 3. TODO комментарии

По всему коду расставлены TODO комментарии:
- В моделях - какие поля могут быть
- В clients - как адаптировать запросы
- В services - как адаптировать парсинг

### 4. Demo/Prod переключение

Простое переключение через `.env`:
```env
USE_DEMO_API=true   # Demo API без токена
# или
USE_DEMO_API=false  # Prod API с токеном
STALCRAFT_API_TOKEN=your_token
```

## Как использовать после получения реального API

### Шаг 1: Тестирование API

```bash
# Отредактировать scripts/test_api.py
REGION = "EU"
ITEM_ID = "real_item_id"  # Реальный ID

# Запустить
python scripts/test_api.py
```

Результат: JSON файлы в `docs/` с реальными ответами.

### Шаг 2: Изучение структуры

Открыть файлы:
- `docs/auction_lots_example_*.json`
- `docs/auction_history_example_*.json`

Изучить поля.

### Шаг 3: Адаптация моделей

В `app/models/auction.py`:
1. Раскомментировать нужные поля
2. Добавить новые поля из JSON
3. Обновить типы если нужно

### Шаг 4: Адаптация парсинга

В `app/services/auction_service.py`:
1. Обновить ключи для извлечения данных
2. Обновить логику парсинга
3. Обновить обработку ошибок

### Шаг 5: Тестирование

```bash
# Запустить сервер
uvicorn app.main:app --reload

# Проверить через frontend или API docs
http://localhost:8000/api/docs
```

## Следующие шаги (после MVP)

### Этап 1.5: Полная интеграция предметов
- Скачать stalcraft-database
- Изучить структуру JSON предметов
- Реализовать items_service методы
- Добавить поиск предметов в frontend
- Добавить иконки предметов

### Этап 2: База данных и аналитика
- PostgreSQL интеграция
- Сбор исторических данных
- Графики цен
- Статистика продаж
- Trends анализ

### Этап 3: Мониторинг и алерты
- Background tasks (Celery)
- Price alerts
- Telegram/Discord боты
- Email notifications
- Watchlist функционал

### Этап 4: Экосистема
- Wiki по предметам
- Крафт калькуляторы
- Гайды и советы
- Community features

## Риски и митигации

### Риск 1: API структура отличается
**Митигация**: Гибкие модели, `extra = "allow"`, TODO комментарии

### Риск 2: Rate limits
**Митигация**: Кэширование (Этап 2), разумные интервалы

### Риск 3: API недоступен
**Митигация**: Обработка ошибок, retry logic, fallback данные

### Риск 4: Большой объем данных
**Митигация**: Pagination, lazy loading, БД для кэша (Этап 2)

## Метрики успеха MVP

- ✅ Сервер запускается без ошибок
- ✅ Frontend загружается и отображается
- ✅ API endpoints отвечают (с моковыми данными OK)
- ✅ Можно выбрать регион
- ✅ Можно ввести item ID
- ✅ Таблицы отображаются (пусть пустые)
- ✅ Документация полная и понятная
- ✅ Docker build работает
- ✅ Код структурирован и читаем
- ✅ Готово к адаптации под реальный API

## Дополнительные улучшения (опционально)

- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Unit tests покрытие
- [ ] Linting в CI
- [ ] Pre-commit hooks
- [ ] Changelog
- [ ] Contributing guide
- [ ] Code of conduct

## Временные оценки

- ✅ Backend структура и API: **ВЫПОЛНЕНО**
- ✅ Frontend базовый: **ВЫПОЛНЕНО**
- ✅ Docker setup: **ВЫПОЛНЕНО**
- ✅ Документация: **ВЫПОЛНЕНО**
- [ ] Тестирование с реальным API: 1-2 часа
- [ ] Адаптация моделей: 1-2 часа
- [ ] Финальные правки: 1-2 часа

**Итого MVP**: Структура готова, остается только адаптация под реальный API (4-6 часов).

## Поддержка

- GitHub: https://github.com/ChillyEz/SC-AUC-Monitoring
- Issues: https://github.com/ChillyEz/SC-AUC-Monitoring/issues
- Docs: https://github.com/ChillyEz/SC-AUC-Monitoring/tree/main/docs

## Заключение

Этап 1 (MVP) предоставляет:
1. ✅ Полную структуру проекта
2. ✅ Работающий backend с API
3. ✅ Функциональный frontend
4. ✅ Гибкую архитектуру
5. ✅ Подробную документацию
6. ✅ Инструменты для тестирования
7. ✅ Готовность к адаптации

Проект готов к получению реальных данных из Stalcraft API и быстрой адаптации под реальную структуру.

---

**Version**: 0.1.0  
**Status**: Базовая структура завершена ✅  
**Next**: Тестирование с реальным Stalcraft API  
**Date**: 2026-01-11
