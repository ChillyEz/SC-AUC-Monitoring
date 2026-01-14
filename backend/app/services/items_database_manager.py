"""
Items Database Manager - Local cache of items from stalcraft-database
"""

import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import httpx

from app.config import settings
from app.models.items import ItemName, ItemSearchResult


class ItemsDatabaseManager:
    """Manager for local cache of items from stalcraft-database"""

    def __init__(self):
        self.cache_dir = Path(__file__).parent.parent.parent / "data" / "items_cache"
        self.cache_file = self.cache_dir / "search_index.json"
        self.metadata_file = self.cache_dir / "metadata.json"

        # In-memory search index: {realm: [items]}
        self.search_index: dict[str, list[dict]] = {}
        # In-memory ID lookup: {realm: {id: item}}
        self.id_lookup: dict[str, dict[str, dict]] = {}
        self.last_update: Optional[datetime] = None

        # Categories to index
        self.categories = [
            "weapon/pistol",
            "weapon/submachine_gun",
            "weapon/assault_rifle",
            "weapon/sniper_rifle",
            "weapon/shotgun",
            "weapon/machine_gun",
            "equipment/outfit",
            "equipment/helmet",
            "equipment/backpack",
            "artifact",
            "consumable",
            "resource",
            "ammo",
        ]

        # Concurrent request limit
        self.max_concurrent_requests = 10

    async def initialize(self, force_update: bool = False) -> None:
        """
        Initialize the database manager

        Args:
            force_update: Force update even if cache is fresh
        """
        # Create cache directory if it doesn't exist
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        if force_update:
            print("⬇️  Downloading items database (forced update)...")
            await self.update_database()
        elif not self._cache_exists():
            print("⬇️  Downloading items database (first run or cache expired)...")
            await self.update_database()
        elif self._cache_expired():
            print("⬇️  Downloading items database (cache expired)...")
            await self.update_database()
        else:
            print("📦 Loading items database from cache...")
            self._load_from_cache()
            print(f"✅ Items database ready! Indexed {self.get_total_items()} items")

    async def update_database(self, realms: Optional[list[str]] = None) -> None:
        """
        Download and index items from GitHub

        Args:
            realms: List of realms to update (default: ["ru", "global"])
        """
        if realms is None:
            realms = ["ru", "global"]

        print(f"📥 Updating database for realms: {', '.join(realms)}")

        # Clear existing index for specified realms
        for realm in realms:
            self.search_index[realm] = []
            self.id_lookup[realm] = {}

        # Download and index items for each realm
        for realm in realms:
            print(f"  → Indexing realm: {realm}")
            realm_items = await self._download_realm_items(realm)
            self.search_index[realm] = realm_items
            # Build ID lookup for O(1) access
            self.id_lookup[realm] = {item["id"]: item for item in realm_items}
            print(f"  ✅ Realm {realm}: {len(realm_items)} items indexed")

        # Update metadata
        self.last_update = datetime.now()

        # Save to cache
        self._save_to_cache()
        print("💾 Database cached successfully!")
        print(f"✅ Items database ready! Indexed {self.get_total_items()} items")

    async def _download_realm_items(self, realm: str) -> list[dict]:
        """
        Download all items for a realm

        Args:
            realm: Realm name (ru, global)

        Returns:
            List of item dictionaries
        """
        items = []
        semaphore = asyncio.Semaphore(self.max_concurrent_requests)

        async def download_category(category: str) -> list[dict]:
            """Download items for a single category"""
            async with semaphore:
                try:
                    category_items = await self._download_category_items(
                        realm, category
                    )
                    print(f"    ✓ {category}: {len(category_items)} items")
                    return category_items
                except Exception as e:
                    print(f"    ✗ {category}: {str(e)}")
                    return []

        # Download all categories concurrently
        tasks = [download_category(category) for category in self.categories]
        results = await asyncio.gather(*tasks)

        # Flatten results
        for category_items in results:
            items.extend(category_items)

        return items

    async def _download_category_items(self, realm: str, category: str) -> list[dict]:
        """
        Download items for a category

        Args:
            realm: Realm name
            category: Category path (e.g., "weapon/pistol")

        Returns:
            List of item dictionaries
        """
        items = []

        # List files in category using GitHub API
        api_url = f"https://api.github.com/repos/{settings.GITHUB_DB_REPO}/contents/{realm}/items/{category}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(api_url, timeout=10.0)
                if response.status_code == 404:
                    return []
                response.raise_for_status()
                files = response.json()

                # Download each item file
                semaphore = asyncio.Semaphore(self.max_concurrent_requests)

                async def download_item(file_info: dict) -> Optional[dict]:
                    """Download a single item"""
                    async with semaphore:
                        if not file_info.get("name", "").endswith(".json"):
                            return None

                        item_id = file_info["name"][:-5]  # Remove .json
                        try:
                            item = await self._download_item(realm, category, item_id)
                            return item
                        except Exception:
                            return None

                tasks = [download_item(file_info) for file_info in files]
                results = await asyncio.gather(*tasks)

                # Filter out None results
                items = [item for item in results if item is not None]

            except Exception:
                # Skip category on error
                pass

        return items

    async def _download_item(self, realm: str, category: str, item_id: str) -> dict:
        """
        Download a single item

        Args:
            realm: Realm name
            category: Category path
            item_id: Item ID

        Returns:
            Item dictionary with indexed fields
        """
        # Download item JSON
        item_url = f"https://raw.githubusercontent.com/{settings.GITHUB_DB_REPO}/{settings.GITHUB_DB_BRANCH}/{realm}/items/{category}/{item_id}.json"

        async with httpx.AsyncClient() as client:
            response = await client.get(item_url, timeout=10.0)
            response.raise_for_status()
            item_data = response.json()

        # Extract name info
        name_obj = ItemName(**item_data.get("name", {}))
        name_ru = ""
        name_en = ""

        if name_obj.type == "translation" and name_obj.lines:
            name_ru = name_obj.lines.get("ru", "")
            name_en = name_obj.lines.get("en", "")
        elif name_obj.type == "text" and name_obj.text:
            name_ru = name_obj.text
            name_en = name_obj.text

        # Build searchable item
        icon_url = f"https://raw.githubusercontent.com/{settings.GITHUB_DB_REPO}/{settings.GITHUB_DB_BRANCH}/{realm}/icons/{category}/{item_id}.png"

        return {
            "id": item_id,
            "name": name_ru or name_en or item_id,
            "category": category,
            "icon_url": icon_url,
            "name_lower": (name_ru or name_en or item_id).lower(),
            "name_ru": name_ru.lower(),
            "name_en": name_en.lower(),
        }

    def search(
        self, query: str, realm: str = "ru", limit: int = 20
    ) -> list[ItemSearchResult]:
        """
        Search items in local database

        Args:
            query: Search query
            realm: Realm name
            limit: Maximum results to return

        Returns:
            List of ItemSearchResult objects
        """
        query_lower = query.lower()
        results = []

        # Get items for realm
        realm_items = self.search_index.get(realm, [])

        # Search through items
        for item in realm_items:
            if len(results) >= limit:
                break

            # Search in ID, RU name, and EN name
            if (
                query_lower in item["id"].lower()
                or query_lower in item["name_lower"]
                or query_lower in item["name_ru"]
                or query_lower in item["name_en"]
            ):
                results.append(
                    ItemSearchResult(
                        id=item["id"],
                        name=item["name"],
                        category=item["category"],
                        icon_url=item["icon_url"],
                    )
                )

        return results

    def get_item_by_id(
        self, item_id: str, realm: str = "ru"
    ) -> Optional[ItemSearchResult]:
        """
        Get item by ID (O(1) lookup)

        Args:
            item_id: Item ID
            realm: Realm name

        Returns:
            ItemSearchResult or None if not found
        """
        # Use O(1) dictionary lookup
        item = self.id_lookup.get(realm, {}).get(item_id)

        if item:
            return ItemSearchResult(
                id=item["id"],
                name=item["name"],
                category=item["category"],
                icon_url=item["icon_url"],
            )

        return None

    def get_total_items(self) -> int:
        """Get total number of indexed items across all realms"""
        return sum(len(items) for items in self.search_index.values())

    def load_from_cache(self) -> None:
        """Public method to load database from cache"""
        self._load_from_cache()

    def is_cache_available(self) -> bool:
        """Public method to check if cache is available"""
        return self._cache_exists()

    def _cache_exists(self) -> bool:
        """Check if cache file exists"""
        return self.cache_file.exists() and self.metadata_file.exists()

    def _cache_expired(self) -> bool:
        """Check if cache is older than 24 hours"""
        if not self._cache_exists():
            return True

        try:
            with open(self.metadata_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)
                last_update = datetime.fromisoformat(metadata.get("last_update", ""))
                return datetime.now() - last_update > timedelta(hours=24)
        except Exception:
            return True

    def _load_from_cache(self) -> None:
        """Load database from cache files"""
        try:
            # Load search index
            with open(self.cache_file, "r", encoding="utf-8") as f:
                self.search_index = json.load(f)

            # Rebuild ID lookup for fast access
            self.id_lookup = {}
            for realm, items in self.search_index.items():
                self.id_lookup[realm] = {item["id"]: item for item in items}

            # Load metadata
            with open(self.metadata_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)
                self.last_update = datetime.fromisoformat(
                    metadata.get("last_update", "")
                )

        except Exception as e:
            print(f"⚠️  Failed to load cache: {str(e)}")
            self.search_index = {}
            self.id_lookup = {}
            self.last_update = None

    def _save_to_cache(self) -> None:
        """Save database to cache files"""
        try:
            # Save search index
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.search_index, f, ensure_ascii=False, indent=2)

            # Save metadata
            metadata = {
                "last_update": (
                    self.last_update.isoformat() if self.last_update else None
                ),
                "total_items": sum(len(items) for items in self.search_index.values()),
            }
            with open(self.metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"⚠️  Failed to save cache: {str(e)}")


# Singleton instance
items_db_manager = ItemsDatabaseManager()
