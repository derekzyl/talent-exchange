
from fastapi.testclient import TestClient

from app.app import init_app

client = TestClient(app=init_app())
