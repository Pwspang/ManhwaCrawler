from starlette.testclient import TestClient

from manhwacrawler.main import app


def test_read_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'hello': 'world'}
