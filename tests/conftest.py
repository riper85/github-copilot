import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=False)
def client():
    """Provide a TestClient and restore the in-memory activities after each test."""
    # Snapshot the original activities so tests remain isolated
    original = copy.deepcopy(app_module.activities)

    with TestClient(app_module.app) as c:
        yield c

    # Restore original state after the test finishes
    app_module.activities = copy.deepcopy(original)

