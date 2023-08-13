from fastapi.testclient import TestClient

from app.server import app

test_client = TestClient(app)
