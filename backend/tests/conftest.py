"""
Pytest configuration and fixtures
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def test_region():
    """Test region"""
    return "EU"


@pytest.fixture
def test_item_id():
    """Test item ID"""
    return "test_item"
