"""
Integration tests for StalcraftAPIClient with different API sources
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from app.config import Settings
from app.clients.stalcraft import StalcraftAPIClient


def test_client_headers_wiki():
    """Test client headers for Wiki API source"""
    # Temporarily set API_SOURCE to wiki
    with patch("app.clients.stalcraft.settings") as mock_settings:
        mock_settings.API_SOURCE = "wiki"
        mock_settings.STALCRAFT_WIKI_API_KEY = "test-wiki-key"
        mock_settings.api_base_url = "https://stalcraft.wiki"

        client = StalcraftAPIClient()
        headers = client._get_headers()

        assert "X-Internal-Key" in headers
        assert headers["X-Internal-Key"] == "test-wiki-key"
        assert "Authorization" not in headers
        assert headers["Content-Type"] == "application/json"


def test_client_headers_demo():
    """Test client headers for Demo API source"""
    with patch("app.clients.stalcraft.settings") as mock_settings:
        mock_settings.API_SOURCE = "demo"
        mock_settings.api_token = "demo-token-123"
        mock_settings.api_base_url = "https://dapi.stalcraft.net"

        client = StalcraftAPIClient()
        headers = client._get_headers()

        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer demo-token-123"
        assert "X-Internal-Key" not in headers
        assert headers["Content-Type"] == "application/json"


def test_client_url_building_wiki():
    """Test URL building for Wiki API"""
    with patch("app.clients.stalcraft.settings") as mock_settings:
        mock_settings.API_SOURCE = "wiki"
        mock_settings.api_base_url = "https://stalcraft.wiki"

        client = StalcraftAPIClient()

        # Test available-lots endpoint
        url = client._build_url("available-lots", "EU", "y1q9")
        assert url == "https://stalcraft.wiki/api/available-lots"

        # Test history endpoint
        url = client._build_url("history", "RU", "abc123")
        assert url == "https://stalcraft.wiki/slug/api/auction-history"


def test_client_url_building_official():
    """Test URL building for official API (demo/production)"""
    with patch("app.clients.stalcraft.settings") as mock_settings:
        mock_settings.API_SOURCE = "demo"
        mock_settings.api_base_url = "https://dapi.stalcraft.net"

        client = StalcraftAPIClient()

        # Test lots endpoint
        url = client._build_url("lots", "EU", "y1q9")
        assert url == "https://dapi.stalcraft.net/EU/auction/y1q9/lots"

        # Test history endpoint
        url = client._build_url("history", "NA", "item456")
        assert url == "https://dapi.stalcraft.net/NA/auction/item456/history"


def test_client_params_wiki():
    """Test params building for Wiki API"""
    with patch("app.clients.stalcraft.settings") as mock_settings:
        mock_settings.API_SOURCE = "wiki"
        mock_settings.api_base_url = "https://stalcraft.wiki"

        client = StalcraftAPIClient()

        # Wiki API always uses region and id params
        params = client._build_params("EU", "y1q9", "available-lots")
        assert params == {"region": "eu", "id": "y1q9"}

        # Even with additional kwargs, Wiki API only uses region and id
        params = client._build_params(
            "RU", "abc123", "history", limit="50", offset="10"
        )
        assert params == {"region": "ru", "id": "abc123"}


def test_client_params_official():
    """Test params building for official API (demo/production)"""
    with patch("app.clients.stalcraft.settings") as mock_settings:
        mock_settings.API_SOURCE = "demo"
        mock_settings.api_base_url = "https://dapi.stalcraft.net"

        client = StalcraftAPIClient()

        # Official API uses kwargs as params
        params = client._build_params(
            "EU", "y1q9", "lots", additional="false", limit="20"
        )
        assert params == {"additional": "false", "limit": "20"}

        # Empty kwargs should return empty dict
        params = client._build_params("EU", "y1q9", "lots")
        assert params == {}


def test_lowercase_region_for_wiki():
    """Test that Wiki API receives lowercase region codes"""
    with patch("app.clients.stalcraft.settings") as mock_settings:
        mock_settings.API_SOURCE = "wiki"
        mock_settings.api_base_url = "https://stalcraft.wiki"

        client = StalcraftAPIClient()

        # Test various region cases
        params = client._build_params("EU", "item1", "lots")
        assert params["region"] == "eu"

        params = client._build_params("RU", "item2", "lots")
        assert params["region"] == "ru"

        params = client._build_params("NA", "item3", "lots")
        assert params["region"] == "na"

        params = client._build_params("SEA", "item4", "lots")
        assert params["region"] == "sea"
