from app.models.product import Product
from app.models.category import Category
from app.models.user import User


def test_guest_access_redirects_to_login(client):
    """Test that unauthorized guests are redirected to login."""
    resp_guest = client.get("/admin/dashboard")
    assert resp_guest.status_code == 302
    assert "/login" in resp_guest.headers["Location"]


def test_customer_forbidden_from_admin(auth_client):
    """Test that regular customers receive 403 Forbidden on admin pages."""
    resp_cust = auth_client.get("/admin/dashboard")
    assert resp_cust.status_code == 403


def test_admin_dashboard_access(admin_client):
    """Test that authenticated admin can access dashboard."""
    resp = admin_client.get("/admin/dashboard")
    assert resp.status_code == 200
    assert b"T\xe1\xbb\x95ng quan h\xe1\xbb\x87 th\xe1\xbb\x91ng" in resp.data


def test_admin_product_crud(admin_client, app):
    """Test admin product CRUD."""
    # Create
    resp = admin_client.post(
        "/admin/products/new",
        data={
            "name": "Omega Seamaster Aqua Terra",
            "price": 140000000,
            "brand": "Omega",
            "category": "Đồng hồ Nam",
            "stock": 7,
            "description": "Chống nước 150m, Master Chronometer",
            "status": "Hiện",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Th\xc3\xaam m\xe1\xbb\x9bi s\xe1\xba\xa3n ph\xe1\xba\xa9m th\xc3\xa0nh c\xc3\xb4ng" in resp.data

    with app.app_context():
        p, _, _ = Product.find_filtered_and_paginated(keyword="Aqua Terra")
        assert len(p) == 1
        prod_id = p[0].id

    # Edit
    resp_edit = admin_client.post(
        f"/admin/products/{prod_id}/edit",
        data={
            "name": "Omega Seamaster Aqua Terra Updated",
            "price": 145000000,
            "brand": "Omega",
            "category": "Đồng hồ Nam",
            "stock": 6,
            "status": "Hiện",
        },
        follow_redirects=True,
    )
    assert resp_edit.status_code == 200
    with app.app_context():
        up = Product.find_by_id(prod_id)
        assert up.name == "Omega Seamaster Aqua Terra Updated"
        assert up.price == 145000000.0

    # Delete
    resp_del = admin_client.post(f"/admin/products/{prod_id}/delete", follow_redirects=True)
    assert resp_del.status_code == 200
    with app.app_context():
        assert Product.find_by_id(prod_id) is None


def test_admin_customer_toggle_lock(admin_client, app):
    """Test admin locking and unlocking a customer account."""
    with app.app_context():
        u = User.find_by_email("customer@gmail.com")
        assert u.isActive is True
        user_id = u.id

    # Lock
    admin_client.post(f"/admin/customers/{user_id}/toggle-lock", follow_redirects=True)
    with app.app_context():
        u_locked = User.find_by_id(user_id)
        assert u_locked.isActive is False

    # Unlock
    admin_client.post(f"/admin/customers/{user_id}/toggle-lock", follow_redirects=True)
    with app.app_context():
        u_unlocked = User.find_by_id(user_id)
        assert u_unlocked.isActive is True
