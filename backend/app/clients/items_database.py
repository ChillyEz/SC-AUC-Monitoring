"""
Items Database Client - fetches item data from stalcraft-database GitHub repository
"""

import httpx
from app.config import settings
from app.models.items import Item, ItemName, ItemSearchResult
from app.core.exceptions import ItemNotFoundError


class ItemsDatabaseClient:
    """Client for interacting with the stalcraft-database GitHub repository"""

    def __init__(self):
        self.base_url = settings.github_db_base_url
        # Categories to search through
        self.categories = [
            "weapon/pistol",
            "weapon/submachine_gun",
            "weapon/assault_rifle",
            "weapon/sniper_rifle",
            "weapon/shotgun",
            "equipment/outfit",
            "equipment/helmet",
            "equipment/backpack",
            "artifact",
            "consumable",
            "resource",
        ]

    def _get_item_url(self, realm: str, category: str, item_id: str) -> str:
        """Generate URL for item JSON file"""
        return f"{self.base_url}/{realm}/items/{category}/{item_id}.json"

    def _get_icon_url(self, realm: str, category: str, item_id: str) -> str:
        """Generate URL for item icon"""
        return f"{self.base_url}/{realm}/icons/{category}/{item_id}.png"

    def _extract_display_name(self, item_name: ItemName) -> str:
        """Extract display name from ItemName object"""
        if item_name.type == "translation" and item_name.lines:
            # Prefer Russian, then English
            if "ru" in item_name.lines:
                return item_name.lines["ru"]
            elif "en" in item_name.lines:
                return item_name.lines["en"]
            # Fallback to first available language
            return next(iter(item_name.lines.values()), "Unknown")
        elif item_name.type == "text" and item_name.text:
            return item_name.text
        return "Unknown"

    async def fetch_item(self, item_id: str, category: str, realm: str = "ru") -> Item:
        """
        Fetch a single item from the database

        Args:
            item_id: Item ID
            category: Item category (e.g., "weapon/pistol")
            realm: Realm (default: "ru")

        Returns:
            Item object

        Raises:
            ItemNotFoundError: If item is not found
        """
        url = self._get_item_url(realm, category, item_id)

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=10.0)
                if response.status_code == 404:
                    raise ItemNotFoundError(
                        f"Item {item_id} not found in category {category}"
                    )
                response.raise_for_status()
                data = response.json()

                # Parse the item
                item = Item(**data)

                # Add display name and icon URL
                item.display_name = self._extract_display_name(item.name)
                item.icon_url = self._get_icon_url(realm, category, item_id)

                return item
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise ItemNotFoundError(
                        f"Item {item_id} not found in category {category}"
                    )
                raise Exception(f"HTTP error fetching item: {str(e)}")
            except Exception as e:
                if isinstance(e, ItemNotFoundError):
                    raise
                raise Exception(f"Error fetching item: {str(e)}")

    async def list_category_items(
        self, category: str, realm: str = "ru"
    ) -> list[ItemSearchResult]:
        """
        List all items in a category using GitHub API

        Args:
            category: Item category (e.g., "weapon/pistol")
            realm: Realm (default: "ru")

        Returns:
            List of ItemSearchResult objects
        """
        # GitHub API URL for directory listing
        api_url = f"https://api.github.com/repos/{settings.GITHUB_DB_REPO}/contents/{realm}/items/{category}"

        items = []
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(api_url, timeout=10.0)
                if response.status_code == 404:
                    return []
                response.raise_for_status()
                files = response.json()

                # Filter JSON files
                for file in files:
                    if file.get("name", "").endswith(".json"):
                        item_id = file["name"][:-5]  # Remove .json extension
                        try:
                            # Fetch full item data
                            item = await self.fetch_item(item_id, category, realm)
                            items.append(
                                ItemSearchResult(
                                    id=item.id,
                                    name=item.display_name or item.id,
                                    category=category,
                                    icon_url=item.icon_url,
                                )
                            )
                        except Exception:
                            # Skip items that fail to fetch
                            continue
            except Exception:
                # Return empty list if category listing fails
                pass

        return items

    async def search_items(
        self, query: str, realm: str = "ru", limit: int = 20
    ) -> list[ItemSearchResult]:
        """
        Search items by name across all categories

        Args:
            query: Search query
            realm: Realm (default: "ru")
            limit: Maximum number of results

        Returns:
            List of ItemSearchResult objects
        """
        query_lower = query.lower()
        results = []

        # Search across all categories
        for category in self.categories:
            if len(results) >= limit:
                break

            try:
                category_items = await self.list_category_items(category, realm)
                for item in category_items:
                    if len(results) >= limit:
                        break
                    # Search in name (case-insensitive)
                    if (
                        query_lower in item.name.lower()
                        or query_lower in item.id.lower()
                    ):
                        results.append(item)
            except Exception:
                # Continue to next category if this one fails
                continue

        return results


# Singleton instance
items_db_client = ItemsDatabaseClient()
