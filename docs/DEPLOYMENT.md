# Deployment Guide

Инструкции по развертыванию SC-AUC-Monitoring

## Варианты развертывания

1. Локальное развертывание (разработка)
2. Docker развертывание (рекомендуется)
3. VPS развертывание (production)

## 1. Локальное развертывание

### Требования
- Python 3.11+
- pip

### Инструкции

```bash
# Клонировать репозиторий
git clone https://github.com/ChillyEz/SC-AUC-Monitoring.git
cd SC-AUC-Monitoring

# Настроить backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Настроить окружение
cp .env.example .env
# Отредактируйте .env

# Запустить сервер
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Или используйте скрипт:
```bash
./scripts/run_dev.sh
```

### Доступ
- Frontend: http://localhost:8000
- API: http://localhost:8000/api/v1
- Docs: http://localhost:8000/api/docs

## 2. Docker развертывание

### Требования
- Docker
- Docker Compose

### Development

```bash
cd docker
docker-compose up
```

Приложение доступно на http://localhost:8000

### Production

```bash
cd docker
docker-compose -f docker-compose.prod.yml up -d
```

### Управление контейнерами

```bash
# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down

# Перезапуск
docker-compose restart

# Rebuild
docker-compose up --build
```

## 3. VPS развертывание (Production)

### Требования
- Ubuntu 20.04+ или другой Linux
- Docker установлен
- Nginx (опционально, для reverse proxy)
- SSL сертификат (рекомендуется)

### Шаг 1: Подготовка сервера

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установка Docker Compose
sudo apt install docker-compose

# Создание пользователя (опционально)
sudo useradd -m -s /bin/bash sc-auc
sudo usermod -aG docker sc-auc
```

### Шаг 2: Клонирование и настройка

```bash
# Клонировать репозиторий
cd /opt
sudo git clone https://github.com/ChillyEz/SC-AUC-Monitoring.git
cd SC-AUC-Monitoring

# Настроить .env
cd backend
sudo cp .env.example .env
sudo nano .env
```

Настройте `.env` для production:
```env
ENV=production
DEBUG=False
USE_DEMO_API=false
STALCRAFT_API_TOKEN=your_production_token
CORS_ORIGINS=["https://yourdomain.com"]
```

### Шаг 3: Запуск с Docker

```bash
cd /opt/SC-AUC-Monitoring/docker
sudo docker-compose -f docker-compose.prod.yml up -d
```

### Шаг 4: Настройка Nginx (Reverse Proxy)

```bash
sudo apt install nginx

# Создать конфигурацию
sudo nano /etc/nginx/sites-available/sc-auc
```

Конфигурация Nginx:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Активировать конфигурацию
sudo ln -s /etc/nginx/sites-available/sc-auc /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Шаг 5: SSL с Let's Encrypt (рекомендуется)

```bash
# Установка Certbot
sudo apt install certbot python3-certbot-nginx

# Получение сертификата
sudo certbot --nginx -d yourdomain.com

# Автообновление
sudo certbot renew --dry-run
```

Nginx автоматически обновит конфигурацию для HTTPS.

### Шаг 6: Настройка автозапуска

Docker Compose с `restart: always` автоматически перезапустит контейнеры.

Systemd service (альтернатива):
```bash
sudo nano /etc/systemd/system/sc-auc.service
```

```ini
[Unit]
Description=SC-AUC-Monitoring
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/SC-AUC-Monitoring/docker
ExecStart=/usr/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/bin/docker-compose -f docker-compose.prod.yml down
User=root

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable sc-auc
sudo systemctl start sc-auc
```

## Переменные окружения (Production)

### Обязательные

```env
ENV=production
DEBUG=False
APP_NAME=SC-AUC-Monitoring
APP_VERSION=0.1.0
```

### Stalcraft API

```env
USE_DEMO_API=false
STALCRAFT_API_TOKEN=your_production_token_here
STALCRAFT_PROD_HOST=eapi.stalcraft.net
```

### CORS

```env
CORS_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]
```

### Будущее (Этап 2)

```env
DATABASE_URL=postgresql://user:password@localhost:5432/sc_auc
REDIS_URL=redis://localhost:6379
```

## Мониторинг и логирование

### Логи Docker

```bash
# Просмотр логов
docker-compose logs -f

# Логи конкретного сервиса
docker-compose logs -f backend

# Последние N строк
docker-compose logs --tail=100 backend
```

### Health Check

```bash
curl http://localhost:8000/health
```

Ожидаемый ответ:
```json
{
  "status": "ok",
  "version": "0.1.0",
  "environment": "production",
  "using_demo_api": false
}
```

### Мониторинг системы

```bash
# CPU и память
docker stats

# Диск
df -h

# Процессы
ps aux | grep uvicorn
```

### Централизованное логирование (опционально)

Настройка Sentry (будущее):
```env
SENTRY_DSN=your_sentry_dsn
```

## Обновление приложения

### Метод 1: Git pull + restart

```bash
cd /opt/SC-AUC-Monitoring
sudo git pull origin main
cd docker
sudo docker-compose -f docker-compose.prod.yml down
sudo docker-compose -f docker-compose.prod.yml up -d --build
```

### Метод 2: Zero-downtime (с Nginx)

```bash
# Build новый образ
docker-compose -f docker-compose.prod.yml build

# Запуск нового контейнера на другом порту
# Обновление Nginx конфигурации
# Остановка старого контейнера
```

## Резервное копирование

### База данных (Этап 2)

```bash
# PostgreSQL backup
docker exec postgres pg_dump -U user sc_auc > backup.sql

# Restore
docker exec -i postgres psql -U user sc_auc < backup.sql
```

### Конфигурация

```bash
# Backup .env
cp backend/.env backend/.env.backup

# Backup Nginx config
sudo cp /etc/nginx/sites-available/sc-auc /backup/
```

## Безопасность

### Firewall

```bash
# UFW настройка
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### Обновления безопасности

```bash
# Автоматические обновления
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### Docker security

```bash
# Запуск как non-root user (в Dockerfile)
USER appuser

# Read-only file system где возможно
# Ограничение ресурсов
```

## Производительность

### Uvicorn workers

В production используйте несколько workers:

`docker-compose.prod.yml`:
```yaml
command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Количество workers: `2-4 × CPU cores`

### Gunicorn (альтернатива)

```bash
pip install gunicorn

gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

## Troubleshooting

### Проблема: Контейнер не запускается

```bash
# Проверка логов
docker-compose logs backend

# Проверка конфигурации
docker-compose config
```

### Проблема: 502 Bad Gateway (Nginx)

```bash
# Проверка статуса backend
curl http://localhost:8000/health

# Проверка Nginx конфигурации
sudo nginx -t

# Проверка логов Nginx
sudo tail -f /var/log/nginx/error.log
```

### Проблема: Высокое использование памяти

```bash
# Проверка
docker stats

# Ограничение памяти в docker-compose.yml
services:
  backend:
    mem_limit: 512m
```

## Чеклист развертывания

- [ ] Сервер подготовлен и обновлен
- [ ] Docker установлен
- [ ] Репозиторий клонирован
- [ ] .env настроен для production
- [ ] Docker контейнеры запущены
- [ ] Nginx настроен
- [ ] SSL сертификат установлен
- [ ] Firewall настроен
- [ ] Health check проходит
- [ ] Логи работают корректно
- [ ] Backup настроен (для Этапа 2)
- [ ] Мониторинг настроен
- [ ] Документация обновлена

## Поддержка

При проблемах:
1. Проверьте логи Docker
2. Проверьте health endpoint
3. Создайте Issue в GitHub

---

**Version**: 0.1.0  
**Last Updated**: 2026-01-11
