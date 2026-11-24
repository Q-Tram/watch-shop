from app.models.order import Order
from app.models.product import Product
from app.services.cart_service import CartService
from app.services.mail_service import MailService


class OrderService:
    """Coordinates checkout flow, stock checks, order snapshotting and email dispatch."""

    @classmethod
    def checkout(cls, user, shipping_info, payment_method="COD", payment_status=None):
        """Execute checkout transaction.

        Returns (success: bool, order_or_error: Order | str, mail_message: str).
        """
        cart = CartService.get_cart_details()
        if cart["is_empty"]:
            return False, "Giỏ hàng đang trống, không thể thanh toán.", ""

        # Validate stock for all items
        for it in cart["items"]:
            prod = Product.find_by_id(it["product_id"])
            if not prod or prod.status == "Ẩn":
                return False, f"Sản phẩm '{it['name']}' không còn tồn tại hoặc đã ngừng bán.", ""
            if prod.stock < it["quantity"]:
                return False, f"Sản phẩm '{it['name']}' chỉ còn {prod.stock} chiếc trong kho.", ""

        # Determine payment status
        if payment_status is None:
            payment_status = "paid" if payment_method == "QR" else "unpaid"

        # Decrement stock
        for it in cart["items"]:
            success = Product.decrement_stock(it["product_id"], it["quantity"])
            if not success:
                return False, f"Lỗi trừ tồn kho sản phẩm '{it['name']}'. Vui lòng thử lại.", ""

        # Create Order snapshot
        order_items = [
            {
                "product": it["product_id"],
                "name": it["name"],
                "price": it["price"],
                "image": it["image"],
                "quantity": it["quantity"],
            }
            for it in cart["items"]
        ]

        order = Order.create(
            user_id=user.id,
            items=order_items,
            shipping_info=shipping_info,
            payment_method=payment_method,
            payment_status=payment_status,
            total_amount=cart["total_amount"],
        )

        # Clear cart
        CartService.clear_cart()

        # Send confirmation email
        mail_sent, mail_msg = MailService.send_order_confirmation(order, user.email)

        return True, order, mail_msg

