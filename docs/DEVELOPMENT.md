# Development Guide

Руководство для разработчиков SC-AUC-Monitoring

## Настройка окружения

### Требования
- Python 3.11 или выше
- Git
- pip / virtualenv

### Первичная настройка

1. **Клонировать репозиторий**
```bash
git clone https://github.com/ChillyEz/SC-AUC-Monitoring.git
cd SC-AUC-Monitoring
```

2. **Создать виртуальное окружение**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. **Установить зависимости**
```bash
pip install -r requirements-dev.txt
```

4. **Настроить окружение**
```bash
cp .env.example .env
# Отредактируйте .env при необходимости
```

5. **Запустить сервер**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Или используйте скрипт:
```bash
cd ..
./scripts/run_dev.sh
```

### Проверка установки

Откройте в браузере:
- Frontend: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- Health: http://localhost:8000/health

## Структура проекта

```
backend/app/
├── main.py              # Entry point
├── config.py            # Configuration
├── api/                 # API endpoints
│   └── v1/
│       ├── router.py    # Main router
│       ├── auction.py   # Auction endpoints
│       └── items.py     # Items endpoints
├── services/            # Business logic
│   ├── auction_service.py
│   └── items_service.py
├── clients/             # External API clients
│   ├── base.py
│   └── stalcraft.py
├── models/              # Domain models
│   ├── auction.py
│   └── items.py
├── schemas/             # Request/Response schemas
│   ├── requests.py
│   └── responses.py
├── core/                # Core utilities
│   ├── exceptions.py
│   └── dependencies.py
└── utils/               # Helper functions
    └── validators.py
```

## Добавление новых функций

### 1. Добавление нового API endpoint

**Шаг 1**: Создать модель (если нужна)
```python
# app/models/your_model.py
from pydantic import BaseModel, Field

class YourModel(BaseModel):
    id: str
    name: str
```

**Шаг 2**: Создать service
```python
# app/services/your_service.py
class YourService:
    async def get_data(self):
        # Business logic here
        pass

your_service = YourService()
```

**Шаг 3**: Создать endpoint
```python
# app/api/v1/your_endpoint.py
from fastapi import APIRouter
from app.services.your_service import your_service

router = APIRouter(prefix="/your-endpoint", tags=["YourTag"])

@router.get("/")
async def get_your_data():
    return await your_service.get_data()
```

**Шаг 4**: Добавить в главный роутер
```python
# app/api/v1/router.py
from app.api.v1 import auction, items, your_endpoint

api_router.include_router(your_endpoint.router)
```

### 2. Добавление нового external API клиента

```python
# app/clients/new_api.py
import httpx
from app.core.exceptions import SCAUCException

class NewAPIClient:
    def __init__(self):
        self.base_url = "https://api.example.com"
    
    async def get_data(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/endpoint")
            response.raise_for_status()
            return response.json()

new_api_client = NewAPIClient()
```

### 3. Добавление frontend компонента

**JavaScript компонент**:
```javascript
// frontend/static/js/components/new-component.js
class NewComponent {
    constructor(element) {
        this.element = element;
        this.init();
    }
    
    init() {
        // Initialization logic
    }
}
```

**CSS стили**:
```css
/* frontend/static/css/components/new-component.css */
.new-component {
    /* Styles */
}
```

**Подключить в index.html**:
```html
<link rel="stylesheet" href="/static/css/components/new-component.css">
<script src="/static/js/components/new-component.js"></script>
```

## Стандарты кодирования

### Python

**Форматирование**:
- Используйте **Black** для автоформатирования
```bash
black app/
```

**Линтинг**:
- Используйте **Ruff** для проверки кода
```bash
ruff check app/
```

**Type hints**:
- Используйте type hints везде
- Проверяйте типы с **mypy**
```bash
mypy app/
```

**Стиль**:
- PEP 8 соблюдение
- Максимальная длина строки: 100 символов
- Docstrings для классов и функций

**Пример**:
```python
from typing import List, Optional

async def get_auction_lots(
    region: str, 
    item_id: str
) -> List[AuctionLot]:
    """
    Получить активные лоты аукциона
    
    Args:
        region: Код региона (EU, RU, NA, SEA)
        item_id: ID предмета
    
    Returns:
        Список активных лотов
    
    Raises:
        InvalidRegionError: Если регион невалиден
    """
    # Implementation
    pass
```

### JavaScript

**Стиль**:
- ES6+ синтаксис
- camelCase для переменных
- PascalCase для классов
- Используйте `const` и `let`, не `var`

**Пример**:
```javascript
class AuctionManager {
    constructor(apiClient) {
        this.apiClient = apiClient;
    }
    
    async fetchLots(region, itemId) {
        try {
            const data = await this.apiClient.getAuctionLots(region, itemId);
            return data;
        } catch (error) {
            console.error('Error fetching lots:', error);
            throw error;
        }
    }
}
```

### CSS

**Методология**: Custom (простой подход для MVP)

**Стиль**:
- kebab-case для классов
- CSS Variables для цветов
- Mobile-first подход

**Пример**:
```css
.auction-table {
    width: 100%;
    border-collapse: collapse;
}

.auction-table__row {
    border-bottom: 1px solid var(--border-color);
}

@media (max-width: 768px) {
    .auction-table {
        font-size: 0.9rem;
    }
}
```

## Тестирование

### Запуск тестов

```bash
cd backend
source venv/bin/activate
pytest
```

### Написание тестов

**Unit test пример**:
```python
# tests/test_services/test_auction_service.py
import pytest
from app.services.auction_service import auction_service

@pytest.mark.asyncio
async def test_get_lots():
    result = await auction_service.get_lots("EU", "test_item")
    assert result.region == "EU"
    assert result.item_id == "test_item"
```

**Integration test пример**:
```python
# tests/test_api/test_auction.py
def test_get_auction_lots(client):
    response = client.get("/api/v1/auction/EU/test_item/lots")
    assert response.status_code == 200
    assert "lots" in response.json()
```

### Coverage

Генерация coverage отчета:
```bash
pytest --cov=app --cov-report=html
# Откройте htmlcov/index.html
```

## Отладка

### Логирование

**Добавить логирование**:
```python
import logging

logger = logging.getLogger(__name__)

logger.info("Processing auction data")
logger.error(f"Error: {error}")
```

### Debug mode

В `.env`:
```env
DEBUG=True
```

### VS Code

`.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app",
                "--reload",
                "--host", "0.0.0.0",
                "--port", "8000"
            ],
            "jinja": true,
            "cwd": "${workspaceFolder}/backend"
        }
    ]
}
```

## Работа с Stalcraft API

### Тестирование API

Используйте скрипт `test_api.py`:
```bash
python scripts/test_api.py
```

Отредактируйте переменные в скрипте:
```python
REGION = "EU"  # Ваш регион
ITEM_ID = "real_item_id"  # Реальный ID предмета
```

### Адаптация моделей

После получения реальных данных:

1. Проверьте JSON в `docs/auction_lots_example_*.json`
2. Обновите модели в `app/models/auction.py`
3. Раскомментируйте нужные поля
4. Обновите парсинг в `app/services/auction_service.py`

## Работа с Items Database

### Скачивание базы

```bash
./scripts/download_items_db.sh
```

База сохраняется в `backend/data/stalcraft-database/`

### Изучение структуры

```bash
cd backend/data/stalcraft-database
ls -R global/items/
```

Пример:
```
global/items/weapons/rifles/ak47.json
global/icons/weapons/rifles/ak47.png
```

### Реализация items_service

После изучения структуры:
1. Обновите `app/models/items.py`
2. Реализуйте методы в `app/services/items_service.py`
3. Добавьте кэширование (опционально)

## Git Workflow

### Ветки

- `main` - production ready код
- `develop` - development ветка
- `feature/*` - новые функции
- `bugfix/*` - исправления

### Commits

Используйте понятные commit messages:
```
feat: Add auction history endpoint
fix: Fix region validation
docs: Update API documentation
refactor: Improve service structure
test: Add tests for auction service
```

### Pull Requests

1. Создайте ветку от `develop`
2. Сделайте изменения
3. Запустите тесты
4. Создайте PR в `develop`
5. После review мерж в `develop`

## Полезные команды

### Backend

```bash
# Запуск сервера с auto-reload
uvicorn app.main:app --reload

# Форматирование кода
black app/

# Проверка кода
ruff check app/

# Type checking
mypy app/

# Тесты
pytest

# Coverage
pytest --cov=app
```

### Docker

```bash
# Build
docker build -f docker/Dockerfile.backend -t sc-auc-backend .

# Run
docker run -p 8000:8000 sc-auc-backend

# Docker Compose
cd docker
docker-compose up
```

## Troubleshooting

### Проблема: ModuleNotFoundError

**Решение**: Убедитесь что virtual environment активирован и зависимости установлены
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Проблема: Port 8000 already in use

**Решение**: Используйте другой порт или освободите 8000
```bash
# Другой порт
uvicorn app.main:app --port 8001

# Найти процесс
lsof -i :8000
kill -9 <PID>
```

### Проблема: CORS errors

**Решение**: Добавьте ваш origin в `.env`
```env
CORS_ORIGINS=["http://localhost:8000","http://localhost:3000"]
```

## Следующие шаги

1. Изучите [ARCHITECTURE.md](ARCHITECTURE.md) для понимания структуры
2. Прочитайте [API.md](API.md) для API documentation
3. Изучите [STALCRAFT_API.md](STALCRAFT_API.md) для работы с Stalcraft API
4. Начните с простых задач из Issues

## Контакты

- GitHub Issues: https://github.com/ChillyEz/SC-AUC-Monitoring/issues

---

**Version**: 0.1.0  
**Last Updated**: 2026-01-11
