# SC-AUC-Monitoring

Веб-платформа для анализа аукциона Stalcraft

## 🎯 Этап 1 (MVP) - Текущий

Базовый просмотр рынка:
- Выбор региона (EU/RU/NA/SEA)
- Выбор предмета
- Просмотр активных лотов
- История продаж

## 🚀 Быстрый старт

### Требования
- Python 3.11+
- pip

### Установка

1. Клонировать репозиторий
```bash
git clone https://github.com/ChillyEz/SC-AUC-Monitoring.git
cd SC-AUC-Monitoring
```

2. Установить зависимости
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Настроить окружение
```bash
cp .env.example .env
# Отредактировать .env при необходимости
```

4. Запустить сервер
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Или использовать скрипт:
```bash
cd ..
./scripts/run_dev.sh
```

5. Открыть в браузере
```
http://localhost:8000
API Docs: http://localhost:8000/api/docs
```

## 📁 Структура проекта

```
SC-AUC-Monitoring/
├── backend/          # FastAPI приложение
│   ├── app/          # Код приложения
│   │   ├── api/      # API endpoints
│   │   ├── clients/  # API клиенты
│   │   ├── models/   # Pydantic модели
│   │   ├── schemas/  # Request/Response schemas
│   │   ├── services/ # Бизнес-логика
│   │   ├── core/     # Ядро (исключения, зависимости)
│   │   └── utils/    # Утилиты
│   ├── tests/        # Тесты
│   ├── requirements.txt
│   └── .env.example
├── frontend/         # HTML/CSS/JS
│   ├── static/       # Статические файлы
│   └── templates/    # HTML шаблоны
├── docker/           # Docker конфигурация
├── docs/             # Документация
└── scripts/          # Утилитарные скрипты
```

## 🔧 Конфигурация

### Demo API (по умолчанию)
```env
USE_DEMO_API=true
```

### Production API
```env
USE_DEMO_API=false
STALCRAFT_API_TOKEN=your_token_here
```

## 🐳 Docker

### Development
```bash
cd docker
docker-compose up
```

### Production
```bash
cd docker
docker-compose -f docker-compose.prod.yml up -d
```

## 📚 Документация

Полная документация в папке `docs/`:
- [API Documentation](docs/API.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [Deployment](docs/DEPLOYMENT.md)
- [Stalcraft API](docs/STALCRAFT_API.md)
- [Stage 1 MVP Plan](docs/STAGE_1_MVP.md)

## 🛠️ Разработка

### Запуск тестов
```bash
cd backend
source venv/bin/activate
pytest
```

### Тестирование Stalcraft API
```bash
python scripts/test_api.py
```

### Скачивание базы предметов
```bash
./scripts/download_items_db.sh
```

## 🛣️ Roadmap

- [x] Этап 1: Базовый просмотр рынка (MVP)
- [ ] Этап 2: Аналитика и хранение данных
- [ ] Этап 3: Мониторинг и сигналы
- [ ] Этап 4: Экосистема (wiki, калькуляторы)

## 🤝 Участие в разработке

Contributions are welcome! См. [DEVELOPMENT.md](docs/DEVELOPMENT.md)

## 📄 Лицензия

MIT License