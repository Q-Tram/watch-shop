from flask import session
from app.models.product import Product

CART_SESSION_KEY = "cart_items"


class CartService:
    """Manages customer shopping cart stored in secure Flask session."""

    @staticmethod
    def get_raw_cart():
        if CART_SESSION_KEY not in session:
            session[CART_SESSION_KEY] = {}
        return session[CART_SESSION_KEY]

    @classmethod
    def get_cart_details(cls):
        raw = cls.get_raw_cart()
        items = []
        total_amount = 0.0
        total_quantity = 0

        for product_id, item_data in list(raw.items()):
            product = Product.find_by_id(product_id)
            if not product or product.status == "Ẩn":
                # Product no longer available
                continue

            qty = int(item_data.get("quantity", 1))
            # Cap at available stock
            if qty > product.stock:
                qty = max(0, product.stock)
                raw[product_id]["quantity"] = qty
                session.modified = True

            if qty <= 0:
                continue

            subtotal = product.price * qty
            total_amount += subtotal
            total_quantity += qty

            items.append({
                "product_id": product.id,
                "name": product.name,
                "price": product.price,
                "image": product.image,
                "brand": product.brand,
                "stock": product.stock,
                "quantity": qty,
                "subtotal": subtotal,
            })

        return {
            "items": items,
            "cart_items": items,
            "total_amount": total_amount,
            "total_quantity": total_quantity,
            "is_empty": len(items) == 0,
        }

    @classmethod
    def add_to_cart(cls, product_id, quantity=1):
        product = Product.find_by_id(product_id)
        if not product or product.status == "Ẩn":
            return False, "Sản phẩm không tồn tại hoặc đã ngừng kinh doanh."

        if product.stock <= 0:
            return False, "Sản phẩm hiện đang hết hàng."

        raw = cls.get_raw_cart()
        current_qty = raw.get(product_id, {}).get("quantity", 0)
        new_qty = current_qty + quantity

        if new_qty > product.stock:
            return False, f"Chỉ còn {product.stock} sản phẩm trong kho."

        raw[product_id] = {
            "quantity": new_qty,
        }
        session.modified = True
        return True, "Đã thêm sản phẩm vào giỏ hàng."

    @classmethod
    def update_quantity(cls, product_id, quantity):
        raw = cls.get_raw_cart()
        if product_id not in raw:
            return False, "Sản phẩm không có trong giỏ hàng."

        if quantity <= 0:
            return cls.remove_from_cart(product_id)

        product = Product.find_by_id(product_id)
        if not product:
            return cls.remove_from_cart(product_id)

        if quantity > product.stock:
            return False, f"Chỉ còn {product.stock} sản phẩm trong kho."

        raw[product_id]["quantity"] = quantity
        session.modified = True
        return True, "Đã cập nhật số lượng."

    @classmethod
    def remove_from_cart(cls, product_id):
        raw = cls.get_raw_cart()
        if product_id in raw:
            del raw[product_id]
            session.modified = True
        return True, "Đã xóa sản phẩm khỏi giỏ hàng."

    @classmethod
    def clear_cart(cls):
        session[CART_SESSION_KEY] = {}
        session.modified = True
        return True
