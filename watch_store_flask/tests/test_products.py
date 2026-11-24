from app.models.product import Product


def test_product_catalog_view(client):
    """Test product catalog displays products."""
    response = client.get("/products")
    assert response.status_code == 200
    assert b"Rolex Submariner Date Test" in response.data


def test_product_search(client, app):
    """Test keyword search functionality."""
    with app.app_context():
        Product.create(
            name="Omega Speedmaster Apollo",
            price=150000000,
            brand="Omega",
            category="Đồng hồ Nam",
            stock=5,
        )

    # Search Omega
    response = client.get("/products?keyword=Omega")
    assert response.status_code == 200
    assert b"Omega Speedmaster Apollo" in response.data
    assert b"Rolex Submariner Date Test" not in response.data


def test_product_filter_by_category(client, app):
    """Test category filter."""
    with app.app_context():
        Product.create(
            name="Cartier Tank Must Nu",
            price=80000000,
            brand="Cartier",
            category="Đồng hồ Nữ",
            stock=3,
        )

    response = client.get("/products", query_string={"category": "Đồng hồ Nữ"})
    assert response.status_code == 200
    assert b"Cartier Tank Must Nu" in response.data


def test_product_detail_view(client, app):
    """Test viewing a product's details."""
    with app.app_context():
        p = Product.get_featured(1)[0]
        prod_id = p.id

    response = client.get(f"/products/{prod_id}")
    assert response.status_code == 200
    assert b"Rolex Submariner Date Test" in response.data
    assert b"300.000.000" in response.data


def test_product_detail_not_found(client):
    """Test non-existent product ID returns 404."""
    response = client.get("/products/507f1f77bcf86cd799439011")
    assert response.status_code == 404
