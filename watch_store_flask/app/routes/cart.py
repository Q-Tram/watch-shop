from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from app.services.cart_service import CartService

cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/cart")
def view_cart():
    """View current shopping cart."""
    cart = CartService.get_cart_details()
    return render_template("cart/index.html", cart=cart)


@cart_bp.route("/cart/add/<product_id>", methods=["POST"])
def add_to_cart(product_id):
    """Add product to cart."""
    if not current_user.is_authenticated:
        flash("Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng.", "warning")
        return redirect(url_for("auth.login", next=url_for("products.detail", product_id=product_id)))

    try:
        quantity = max(1, int(request.form.get("quantity", 1)))
    except (ValueError, TypeError):
        quantity = 1

    success, msg = CartService.add_to_cart(product_id, quantity)
    if success:
        flash(msg, "success")
    else:
        flash(msg, "warning")

    referrer = request.referrer
    if referrer and ("products" in referrer or "cart" in referrer):
        return redirect(referrer)
    return redirect(url_for("cart.view_cart"))


@cart_bp.route("/cart/update/<product_id>", methods=["POST"])
def update_quantity(product_id):
    """Update item quantity in cart."""
    try:
        quantity = int(request.form.get("quantity", 1))
    except (ValueError, TypeError):
        quantity = 1

    success, msg = CartService.update_quantity(product_id, quantity)
    if success:
        flash(msg, "success")
    else:
        flash(msg, "warning")
    return redirect(url_for("cart.view_cart"))


@cart_bp.route("/cart/remove/<product_id>", methods=["POST"])
def remove_from_cart(product_id):
    """Remove item from cart."""
    CartService.remove_from_cart(product_id)
    flash("Đã xóa sản phẩm khỏi giỏ hàng.", "info")
    return redirect(url_for("cart.view_cart"))


@cart_bp.route("/cart/clear", methods=["POST"])
def clear_cart():
    """Empty the entire shopping cart."""
    CartService.clear_cart()
    flash("Giỏ hàng đã được làm trống.", "info")
    return redirect(url_for("cart.view_cart"))

