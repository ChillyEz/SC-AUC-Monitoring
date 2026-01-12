#!/usr/bin/env python3
"""
Скрипт для тестирования Stalcraft API
Помогает определить структуру ответов
"""
import asyncio
import httpx
import json
from pathlib import Path
import sys

# Добавить backend в путь
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# Import после изменения sys.path
from app.config import settings


async def test_auction_lots(region: str, item_id: str):
    """Тест получения лотов"""
    url = f"{settings.api_base_url}/{region}/auction/{item_id}/lots"
    
    # Параметры запроса согласно документации API
    params = {
        "additional": "false",
        "limit": "20",
        "offset": "0",
        "order": "desc",
        "sort": "time_created"
    }
    
    headers = {"Content-Type": "application/json"}
    if not settings.USE_DEMO_API and settings.STALCRAFT_API_TOKEN:
        headers["Authorization"] = f"Bearer {settings.STALCRAFT_API_TOKEN}"

    print(f"Testing: {url}")
    print(f"Params: {params}")
    print(f"Headers: {headers}")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=10.0)
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print("Response JSON:")
                print(json.dumps(data, indent=2, ensure_ascii=False))

                # Сохранить в файл
                output_file = (
                    Path(__file__).parent.parent
                    / "docs"
                    / f"auction_lots_example_{region}_{item_id}.json"
                )
                output_file.write_text(json.dumps(data, indent=2, ensure_ascii=False))
                print(f"\nSaved to: {output_file}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Exception: {e}")


async def test_auction_history(region: str, item_id: str):
    """Тест получения истории"""
    url = f"{settings.api_base_url}/{region}/auction/{item_id}/history"
    
    # Параметры запроса согласно документации API
    params = {
        "additional": "false",
        "limit": "20",
        "offset": "0"
    }
    
    headers = {"Content-Type": "application/json"}
    if not settings.USE_DEMO_API and settings.STALCRAFT_API_TOKEN:
        headers["Authorization"] = f"Bearer {settings.STALCRAFT_API_TOKEN}"

    print(f"\nTesting: {url}")
    print(f"Params: {params}")
    print(f"Headers: {headers}")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=10.0)
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print("Response JSON:")
                print(json.dumps(data, indent=2, ensure_ascii=False))

                # Сохранить в файл
                output_file = (
                    Path(__file__).parent.parent
                    / "docs"
                    / f"auction_history_example_{region}_{item_id}.json"
                )
                output_file.write_text(json.dumps(data, indent=2, ensure_ascii=False))
                print(f"\nSaved to: {output_file}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Exception: {e}")


if __name__ == "__main__":
    # Используйте реальный ID предмета из stalcraft-database
    REGION = "EU"  # EU, RU, NA, SEA
    ITEM_ID = "y1q9"  # Пример: можно заменить на реальный ID предмета

    print("=== Stalcraft API Test ===")
    print(f"API URL: {settings.api_base_url}")
    print(f"Using Demo API: {settings.USE_DEMO_API}")
    print(f"Region: {REGION}")
    print(f"Item ID: {ITEM_ID}")
    print("=" * 50)

    asyncio.run(test_auction_lots(REGION, ITEM_ID))
    asyncio.run(test_auction_history(REGION, ITEM_ID))
