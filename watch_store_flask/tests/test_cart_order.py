from app.models.product import Product
from app.models.order import Order
from app.models.user import User


def test_cart_workflow(auth_client, app):
    """Test full shopping cart flow: add, update, remove, clear."""
    with app.app_context():
        p = Product.get_featured(1)[0]
        prod_id = p.id

    # 1. Add to cart
    resp = auth_client.post(
        f"/cart/add/{prod_id}",
        data={"quantity": 2},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"\xc4\x90\xc3\xa3 th\xc3\xaam s\xe1\xba\xa3n ph\xe1\xba\xa9m v\xc3\xa0o gi\xe1\xbb\x8f h\xc3\xa0ng" in resp.data

    # 2. View cart
    resp = auth_client.get("/cart")
    assert resp.status_code == 200
    assert b"Rolex Submariner Date Test" in resp.data
    assert b"600.000.000" in resp.data  # 2 x 300,000,000

    # 3. Update quantity
    resp = auth_client.post(
        f"/cart/update/{prod_id}",
        data={"quantity": 1},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"300.000.000" in resp.data

    # 4. Remove item
    resp = auth_client.post(
        f"/cart/remove/{prod_id}",
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Gi\xe1\xbb\x8f h\xc3\xa0ng c\xe1\xbb\xa7a b\xe1\xba\xa1n \xc4\x91ang tr\xe1\xbb\x91ng" in resp.data


def test_checkout_and_order_creation(auth_client, app):
    """Test full checkout flow, stock reduction, and snapshot integrity."""
    with app.app_context():
        p = Product.get_featured(1)[0]
        prod_id = p.id
        initial_stock = p.stock

    # Add 2 items to cart
    auth_client.post(f"/cart/add/{prod_id}", data={"quantity": 2})

    # Submit checkout
    resp = auth_client.post(
        "/checkout",
        data={
            "fullName": "Nguyen Van B",
            "phone": "0911223344",
            "address": "789 Tran Hung Dao, Quan 5, TP.HCM",
            "note": "Giao buoi sang",
            "paymentMethod": "COD",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"\xc4\x90\xe1\xba\xb7t h\xc3\xa0ng th\xc3\xa0nh c\xc3\xb4ng" in resp.data

    # Verify inventory was decremented
    with app.app_context():
        updated_p = Product.find_by_id(prod_id)
        assert updated_p.stock == initial_stock - 2

        # Verify Order document created
        orders, total, _ = Order.find_all_paginated()
        assert total >= 1
        latest_order = orders[0]
        assert latest_order.shippingInfo["fullName"] == "Nguyen Van B"
        assert latest_order.totalAmount == 600000000.0
        assert latest_order.paymentMethod == "COD"
        assert latest_order.orderStatus == "pending"

        # Change original product name and price
        Product.update(prod_id, name="Renamed Rolex", price=999999999)

        # Verify Order snapshot remains unchanged!
        refreshed_order = Order.find_by_id(latest_order.id)
        assert refreshed_order.items[0]["name"] == "Rolex Submariner Date Test"
        assert refreshed_order.items[0]["price"] == 300000000.0


def test_user_cannot_view_others_orders(client, auth_client, app):
    """Test access control: customers cannot view orders belonging to others."""
    # 1. Create an order for a second customer
    with app.app_context():
        other_user = User.create(
            fullName="Other User",
            email="other@gmail.com",
            password="password123",
            role="customer",
        )
        p = Product.get_featured(1)[0]
        other_order = Order.create(
            user_id=other_user.id,
            items=[{"product": p.id, "name": p.name, "price": p.price, "quantity": 1}],
            shipping_info={"fullName": "Other", "phone": "0900", "address": "Hue"},
            total_amount=p.price,
        )
        order_id = other_order.id

    # 2. auth_client (logged in as customer@gmail.com) tries to view other_order
    resp = auth_client.get(f"/my-orders/{order_id}")
    assert resp.status_code == 403
