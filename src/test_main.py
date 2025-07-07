
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

"""Test /api/weather with no filters"""
def test_weather_post_without_filters():
    response = client.post("/api/weather", json={"page": 1})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "total_results" in data
    assert isinstance(data["results"], list)

"""Test /api/weather with filters station_id and date"""
def test_weather_post_with_filters():
    response = client.post("/api/weather", json={
        "station_id": "USC00110072",
        "date": "1985-01-01",
        "page": 1
    })
    assert response.status_code == 200
    assert "results" in response.json()

"""Test /api/weather/stats with no filters"""
def test_weather_stats_post_without_filters():
    response = client.post("/api/weather/stats", json={"page": 1})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "total_pages" in data

"""Test /api/weather/stats with filters station_id and year"""
def test_weather_stats_post_with_filters():
    response = client.post("/api/weather/stats", json={
        "station_id": "USC00110072",
        "year": 1985,
        "page": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["results"], list)
