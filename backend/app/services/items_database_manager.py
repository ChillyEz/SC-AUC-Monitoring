"""
Items Database Manager - manages local cache of stalcraft-database
"""
import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import httpx

from app.config import settings


class ItemsDatabaseManager:
    """
    Manages local cache of items from stalcraft-database
    Downloads and indexes items for fast search
    """

    def __init__(self):
        self.cache_dir = Path("data/items_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.index_file = self.cache_dir / "search_index.json"
        self.metadata_file = self.cache_dir / "metadata.json"

        # In-memory search index
        self.search_index = {}  # {realm: [{id, name, category, icon_url}, ...]}
        self.last_update = None

        # GitHub configuration
        self.github_repo = settings.GITHUB_DB_REPO
        self.github_branch = settings.GITHUB_DB_BRANCH
        self.raw_base_url = f"https://raw.githubusercontent.com/{self.github_repo}/{self.github_branch}"
        self.api_base_url = f"https://api.github.com/repos/{self.github_repo}/contents"

        # Categories to index
        self.categories = [
            # Оружие
            "weapon/assault_rifle",
            "weapon/device",  # Устройства (детекторы и т.д.)
            "weapon/heavy",  # Тяжёлое оружие
            "weapon/machine_gun",
            "weapon/melee",  # Ближний бой
            "weapon/pistol",
            "weapon/shotgun_rifle",
            "weapon/sniper_rifle",
            "weapon/submachine_gun",
            # Броня
            "armor/clothes",  # Одежда
            "armor/combat",  # Боевая броня
            "armor/combined",  # Комбинированная
            "armor/device",  # Устройства брони
            "armor/scientist",  # Научная броня
            # Остальное
            "artefact",  # Артефакты (с подпапками)
            "attachment",  # Модули оружия (с подпапками)
            "weapon_modules",  # Модули оружия - альтернатива (с подпапками)
            "backpacks",
            "containers",
            "bullet",  # Патроны
            "grenade",
            "medicine",
            "food",
            "drink",
            "misc",  # Разное
            "other",  # Прочее
        ]

    async def initialize(self, force_update:  bool = False):
        """Initialize database - load from cache or download"""
        if force_update: 
            print("🔄 Force updating items database...")
            await self.update_database()
        elif self._cache_exists() and not self._cache_expired():
            print("📦 Loading items database from cache...")
            self._load_from_cache()
        else:
            print("⬇️  Downloading items database (first run or cache expired)...")
            await self.update_database()

        total_items = sum(len(items) for items in self.search_index.values())
        print(f"✅ Items database ready!  Indexed {total_items} items")

    def _cache_exists(self) -> bool:
        """Check if cache exists"""
        return self.index_file.exists() and self.metadata_file.exists()

    def _cache_expired(self) -> bool:
        """Check if cache is older than 24 hours"""
        if not self.metadata_file.exists():
            return True

        try: 
            metadata = json.loads(self.metadata_file.read_text(encoding="utf-8"))
            last_update = datetime.fromisoformat(metadata["last_update"])
            return datetime.now() - last_update > timedelta(hours=24)
        except Exception:
            return True

    def _load_from_cache(self):
        """Load search index from cache"""
        try: 
            self.search_index = json.loads(
                self.index_file.read_text(encoding="utf-8")
            )
            metadata = json.loads(self.metadata_file.read_text(encoding="utf-8"))
            self.last_update = datetime.fromisoformat(metadata["last_update"])
        except Exception as e: 
            print(f"⚠️  Failed to load cache:  {e}")
            self.search_index = {}

    def _save_to_cache(self):
        """Save search index to cache"""
        try:
            self.index_file.write_text(
                json.dumps(self.search_index, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            metadata = {
                "last_update": datetime.now().isoformat(),
                "total_items": sum(
                    len(items) for items in self.search_index.values()
                ),
                "realms": list(self.search_index.keys()),
            }
            self.metadata_file.write_text(
                json.dumps(metadata, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception as e: 
            print(f"⚠️  Failed to save cache: {e}")

    async def update_database(self, realms: list[str] | None = None):
        """
        Download and index items database

        Args:
            realms:  List of realms to update (default: ["ru", "global"])
        """
        if realms is None:
            realms = ["ru", "global"]

        print(f"📥 Updating database for realms: {', '.join(realms)}")

        for realm in realms:
            print(f"  → Indexing realm: {realm}")
            realm_items = []

            for category in self.categories:
                try:
                    items = await self._index_category(realm, category)
                    realm_items.extend(items)
                    print(f"    ✓ {category}:  {len(items)} items")
                except Exception as e:
                    print(f"    ✗ {category}: {e}")
                    continue

            self.search_index[realm] = realm_items
            print(f"  ✅ Realm {realm}: {len(realm_items)} items indexed")

        self.last_update = datetime.now()
        self._save_to_cache()
        print("💾 Database cached successfully!")

    async def _index_category(
        self, realm: str, category: str
    ) -> list[dict[str, Any]]:
        """Index all items in a category"""
        # Get list of item IDs in category (handles subdirectories recursively)
        item_ids = await self._get_category_item_ids(realm, category)

        items = []
        # Batch download items (limit concurrent requests)
        semaphore = asyncio.Semaphore(10)  # Max 10 concurrent requests

        async def fetch_item(item_id: str):
            async with semaphore:
                try:
                    item_data = await self._fetch_item_data(realm, category, item_id)
                    if item_data:
                        items.append(item_data)
                except Exception:
                    pass  # Skip failed items

        await asyncio.gather(*[fetch_item(item_id) for item_id in item_ids])

        return items

    async def _get_category_item_ids(self, realm: str, category: str) -> list[str]:
        """
        Get list of item IDs in a category from GitHub API
        Handles both direct files AND subdirectories recursively
        Skips service directories like _variants, _deprecated
        """
        url = f"{self.api_base_url}/{realm}/items/{category}"
        headers = {"Accept": "application/vnd.github+json"}

        # Use GitHub token if provided
        if settings.GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            data = response.json()

            item_ids = []
            subdirs = []

            # Process both files and directories
            for item in data:
                if item["type"] == "file" and item["name"].endswith(".json"):
                    # Direct file in root - extract ID
                    item_ids.append(item["name"].replace(".json", ""))
                elif item["type"] == "dir": 
                    # Skip service directories
                    if item["name"] in ["_variants", "_deprecated"]:
                        #отладка
                        print(f"    [DEBUG] {category}: Skipping service directory {item['name']}")
                        continue
                    # Valid subdirectory - explore it
                    subdirs.append(item["name"])

            print(f"    [DEBUG] {category}: Found {len(item_ids)} direct files")
            print(f"    [DEBUG] {category}: Found {len(subdirs)} subdirectories")

            # If we found subdirectories, recursively fetch from them
            if subdirs: 
                print(f"       → {category}:  Found {len(subdirs)} subdirectories")

                for subdir in subdirs:
                    subdir_url = (
                        f"{self.api_base_url}/{realm}/items/{category}/{subdir}"
                    )
                    try: 
                        sub_response = await client.get(
                            subdir_url, headers=headers, timeout=30.0
                        )
                        sub_response.raise_for_status()
                        sub_data = sub_response.json()

                        # Extract IDs from subdirectory
                        subdir_files = 0
                        for sub_item in sub_data:
                            if (
                                sub_item["type"] == "file"
                                and sub_item["name"].endswith(".json")
                            ):
                                # Store with subdirectory:  "subdir/itemid"
                                item_id = (
                                    f"{subdir}/{sub_item['name'].replace('.json', '')}"
                                )
                                item_ids.append(item_id)
                                subdir_files += 1

                        # Print only if files found
                        if subdir_files > 0:
                            print(f"         └─ {subdir}: {subdir_files} items")
                    except Exception as e:
                        print(f"         └─ {subdir}:  ERROR - {e}")

            #отладка
            print(f"    [DEBUG] {category}: Total item IDs found: {len(item_ids)}")

            return item_ids

    async def _fetch_item_data(
        self, realm: str, category: str, item_id:  str
    ) -> dict[str, Any] | None:
        """
        Fetch item data and extract searchable info
        Handles items in subdirectories (item_id can be "subdir/id")
        """
        url = f"{self.raw_base_url}/{realm}/items/{category}/{item_id}.json"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                data = response.json()

                # Extract display name
                name_obj = data.get("name", {})
                # Use only the item ID part (without subdirectory) as fallback
                display_name = item_id.split("/")[-1]
                lines = {}  # Инициализация lines для использования ниже

                if name_obj.get("type") == "translation":
                    lines = name_obj.get("lines", {})
                    display_name = lines.get("ru") or lines.get("en", display_name)
                elif name_obj.get("type") == "text":
                    display_name = name_obj.get("text", display_name)

                # Build searchable item
                return {
                    "id": item_id,  # Сохраняем полный путь (с подпапкой если есть)
                    "name": display_name,
                    "category": category,
                    "icon_url":  f"{self.raw_base_url}/{realm}/icons/{category}/{item_id}.png",
                    # Store name variants for search
                    "name_lower": display_name.lower(),
                    "name_ru": lines.get("ru", "").lower(),
                    "name_en": lines.get("en", "").lower(),
                }
        except Exception:
            return None

    def search(
        self, query: str, realm: str = "ru", limit:  int = 20
    ) -> list[dict[str, Any]]:
        """
        Fast local search in indexed items

        Args:
            query: Search query
            realm: Realm to search in
            limit: Maximum number of results

        Returns:
            List of matching items
        """
        if realm not in self.search_index:
            return []

        query_lower = query.lower()
        results = []

        for item in self.search_index[realm]:
            # Search in name, ID, or translated names
            if (
                query_lower in item["name_lower"]
                or query_lower in item["id"].lower()
                or (item["name_ru"] and query_lower in item["name_ru"])
                or (item["name_en"] and query_lower in item["name_en"])
            ):
                results.append(
                    {
                        "id": item["id"],
                        "name": item["name"],
                        "category": item["category"],
                        "icon_url": item["icon_url"],
                    }
                )

                if len(results) >= limit:
                    break

        return results

    def get_item_by_id(
        self, item_id: str, realm: str = "ru"
    ) -> dict[str, Any] | None:
        """Get item by ID from index"""
        if realm not in self.search_index:
            return None

        for item in self.search_index[realm]:
            if item["id"] == item_id: 
                return {
                    "id": item["id"],
                    "name": item["name"],
                    "category": item["category"],
                    "icon_url": item["icon_url"],
                }

        return None


# Singleton
items_db_manager = ItemsDatabaseManager()