import pytest
from rest_framework.test import APIClient

from ..api_client import PrefixedAPIClient


@pytest.fixture
def client() -> APIClient:
    return PrefixedAPIClient(prefix="/api/v1")
