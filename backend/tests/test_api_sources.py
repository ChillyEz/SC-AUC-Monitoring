"""
Tests for API source configuration and switching
"""

import pytest
import os
from app.config import Settings


def test_wiki_api_source():
    """Test Wiki API source configuration"""
    settings = Settings(API_SOURCE="wiki")

    assert settings.API_SOURCE == "wiki"
    assert settings.api_base_url == "https://stalcraft.wiki"
    assert settings.api_token == ""


def test_demo_api_source():
    """Test Demo API source configuration"""
    settings = Settings(API_SOURCE="demo")

    assert settings.API_SOURCE == "demo"
    assert settings.api_base_url == "https://dapi.stalcraft.net"
    assert settings.api_token != ""


def test_production_api_source():
    """Test Production API source configuration"""
    settings = Settings(API_SOURCE="production", STALCRAFT_PROD_TOKEN="test_token")

    assert settings.API_SOURCE == "production"
    assert settings.api_base_url == "https://eapi.stalcraft.net"
    assert settings.api_token == "test_token"


def test_api_base_url_switching():
    """Test that api_base_url switches correctly based on API_SOURCE"""
    wiki_settings = Settings(API_SOURCE="wiki")
    assert wiki_settings.api_base_url == "https://stalcraft.wiki"

    demo_settings = Settings(API_SOURCE="demo")
    assert demo_settings.api_base_url == "https://dapi.stalcraft.net"

    prod_settings = Settings(API_SOURCE="production")
    assert prod_settings.api_base_url == "https://eapi.stalcraft.net"


def test_api_token_switching():
    """Test that api_token switches correctly based on API_SOURCE"""
    wiki_settings = Settings(API_SOURCE="wiki")
    assert wiki_settings.api_token == ""

    demo_settings = Settings(API_SOURCE="demo")
    assert demo_settings.api_token != ""
    assert demo_settings.api_token == demo_settings.STALCRAFT_DEMO_TOKEN

    prod_settings = Settings(API_SOURCE="production", STALCRAFT_PROD_TOKEN="test_token")
    assert prod_settings.api_token == "test_token"


def test_health_endpoint(client):
    """Test health endpoint returns api_source"""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert "api_source" in data
    assert data["api_source"] in ["demo", "production", "wiki"]
    assert "using_demo_api" in data
    assert isinstance(data["using_demo_api"], bool)
    assert data["using_demo_api"] == (data["api_source"] == "demo")
