import json


def test_api_products_list(client):
    """Test REST API endpoint GET /api/v1/products."""
    resp = client.get("/api/v1/products")
    assert resp.status_code == 200
    data = json.loads(resp.data.decode("utf-8"))
    assert data["status"] == "success"
    assert "data" in data
    assert "pagination" in data
    assert len(data["data"]) >= 1
    assert data["data"][0]["name"] == "Rolex Submariner Date Test"


def test_api_exchange_rate(client):
    """Test network integration endpoint GET /api/v1/exchange-rate."""
    resp = client.get("/api/v1/exchange-rate")
    assert resp.status_code == 200
    data = json.loads(resp.data.decode("utf-8"))
    assert data["status"] == "success"
    assert "data" in data
    assert data["data"]["base"] == "USD"
    assert float(data["data"]["rate_vnd"]) > 0


def test_api_banks_list(client):
    """Test network integration endpoint GET /api/v1/banks."""
    resp = client.get("/api/v1/banks")
    assert resp.status_code == 200
    data = json.loads(resp.data.decode("utf-8"))
    assert data["status"] == "success"
    assert "banks" in data["data"]
    assert len(data["data"]["banks"]) >= 1

