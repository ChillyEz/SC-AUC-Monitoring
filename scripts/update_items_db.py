#!/usr/bin/env python3
"""
CLI tool to update items database

Usage:
    python scripts/update_items_db.py --force
    python scripts/update_items_db.py --realms ru --force
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.services.items_database_manager import items_db_manager  # noqa: E402


async def main():
    parser = argparse.ArgumentParser(
        description="Update items database from stalcraft-database"
    )
    parser.add_argument(
        "--realms",
        nargs="+",
        default=["ru", "global"],
        help="List of realms to update (default: ru global)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force update even if cache is fresh",
    )

    args = parser.parse_args()

    print("🚀 SC-AUC-Monitoring Items Database Updater")
    print("=" * 50)

    try:
        if args.force or not items_db_manager.is_cache_available():
            print(f"📥 Updating database for realms: {', '.join(args.realms)}")
            await items_db_manager.update_database(args.realms)
        else:
            print("📦 Cache exists and is fresh. Use --force to update anyway.")
            items_db_manager._load_from_cache()
            total_items = sum(
                len(items) for items in items_db_manager.search_index.values()
            )
            print(f"✅ Database loaded from cache. Total items: {total_items}")

        print("=" * 50)
        print("✅ Done!")

    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
