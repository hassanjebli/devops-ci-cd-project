import json
from app.app import app

def test_get_stats_api():
    client = app.test_client()
    response = client.get("/api/stats")
    assert response.status_code == 200
    assert "total_tasks" in response.json
    assert "message" in response.json
    assert isinstance(response.json["total_tasks"], int)
