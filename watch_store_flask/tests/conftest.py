import os
import sys
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.db import get_db
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.setting import Setting


@pytest.fixture(scope="session")
def app():
    """Create Flask test application configured for testing with in-memory Mongo."""
    test_app = create_app("testing")
    return test_app


@pytest.fixture(autouse=True)
def clean_database(app):
    """Clean and seed database before each test."""
    with app.app_context():
        db = get_db()
        for col_name in ["users", "categories", "products", "orders", "settings"]:
            try:
                db[col_name].delete_many({})
            except Exception:
                pass

        # Seed essential admin and customer
        User.create(
            fullName="Super Admin",
            email="admin@gmail.com",
            password="adminpassword123",
            role="admin",
        )
        User.create(
            fullName="Test Customer",
            email="customer@gmail.com",
            password="customerpassword123",
            phone="0912345678",
            address="456 Nguyen Hue, Quan 1, TP.HCM",
            role="customer",
        )
        # Seed test product
        Product.create(
            name="Rolex Submariner Date Test",
            price=300000000,
            brand="Rolex",
            category="Đồng hồ Nam",
            stock=10,
            image="https://example.com/rolex.jpg",
            description="Đồng hồ lặn chuyên nghiệp chịu nước 300m",
            status="Hiện",
        )
        # Seed category
        Category.create(name="Đồng hồ Nam", description="Dành cho phái mạnh")
        # Seed settings
        Setting.get_website_settings()
        Setting.get_payment_settings()


@pytest.fixture
def client(app):
    """Test client for HTTP requests."""
    return app.test_client()


@pytest.fixture
def auth_client(client):
    """Client authenticated as regular customer."""
    client.post(
        "/login",
        data={"email": "customer@gmail.com", "password": "customerpassword123"},
        follow_redirects=True,
    )
    return client


@pytest.fixture
def admin_client(client):
    """Client authenticated as administrator."""
    client.post(
        "/login",
        data={"email": "admin@gmail.com", "password": "adminpassword123"},
        follow_redirects=True,
    )
    return client

