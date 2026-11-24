import urllib.parse
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.forms.order_forms import CheckoutForm
from app.models.order import Order
from app.models.setting import Setting
from app.services.cart_service import CartService
from app.services.order_service import OrderService

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    """Checkout page: shipping details, payment method (COD / QR), order creation."""
    cart = CartService.get_cart_details()
    if cart["is_empty"]:
        flash("Giỏ hàng của bạn đang trống. Vui lòng chọn sản phẩm trước khi thanh toán.", "warning")
        return redirect(url_for("products.catalog"))

    payment_settings = Setting.get_payment_settings()

    form = CheckoutForm()
    # Pre-populate default values from user profile on GET
    if request.method == "GET":
        form.fullName.data = current_user.fullName
        form.phone.data = current_user.phone
        form.address.data = current_user.address

    # Build QR payment payload string
    bank_name = payment_settings.get("bankName", "MB BANK")
    acc_num = payment_settings.get("accountNumber", "123456789")
    acc_name = payment_settings.get("accountName", "WATCH STORE")
    note = payment_settings.get("transferContent", "Thanh toan don hang WatchStore")
    amount = int(cart["total_amount"])

    qr_payload = f"WATCHSTORE|BANK:{bank_name}|ACCOUNT:{acc_num}|NAME:{acc_name}|AMOUNT:{amount}|NOTE:{note}"
    # Generate VietQR quick image URL if no custom image is configured
    custom_qr_image = payment_settings.get("qrImage", "")
    if not custom_qr_image:
        # Standard VietQR link format: https://img.vietqr.io/image/<BANK>-<ACCOUNT>-compact2.jpg?amount=<AMOUNT>&addInfo=<NOTE>&accountName=<NAME>
        encoded_note = urllib.parse.quote(note)
        encoded_acc_name = urllib.parse.quote(acc_name)
        qr_image_url = f"https://img.vietqr.io/image/{bank_name.replace(' ', '')}-{acc_num}-compact2.jpg?amount={amount}&addInfo={encoded_note}&accountName={encoded_acc_name}"
    else:
        qr_image_url = custom_qr_image

    if form.validate_on_submit():
        shipping_info = {
            "fullName": form.fullName.data,
            "phone": form.phone.data,
            "address": form.address.data,
            "note": form.note.data or "",
        }
        payment_method = form.paymentMethod.data
        qr_paid = request.form.get("qr_paid_confirmed") == "1"

        payment_status = "paid" if (payment_method == "QR" and qr_paid) else "unpaid"

        success, order_or_err, mail_msg = OrderService.checkout(
            user=current_user,
            shipping_info=shipping_info,
            payment_method=payment_method,
            payment_status=payment_status,
        )

        if not success:
            flash(order_or_err, "danger")
            return redirect(url_for("orders.checkout"))

        order = order_or_err
        flash("Đặt hàng thành công! Cảm ơn quý khách.", "success")
        if mail_msg:
            flash(mail_msg, "info")

        return redirect(url_for("orders.success", order_id=order.id))

    return render_template(
        "orders/checkout.html",
        form=form,
        cart=cart,
        payment_settings=payment_settings,
        qr_payload=qr_payload,
        qr_image_url=qr_image_url,
    )


@orders_bp.route("/order-success/<order_id>")
@login_required
def success(order_id):
    """Order confirmation screen."""
    order = Order.find_by_id(order_id)
    if not order or (order.user_id != current_user.id and not current_user.is_admin):
        abort(404)

    return render_template("orders/success.html", order=order)


@orders_bp.route("/my-orders")
@login_required
def my_orders():
    """List of customer's own orders."""
    try:
        page = max(1, int(request.args.get("page", 1)))
    except (ValueError, TypeError):
        page = 1

    orders, total_count, total_pages = Order.find_by_user(
        user_id=current_user.id,
        page=page,
        per_page=10,
    )

    return render_template(
        "orders/list.html",
        orders=orders,
        page=page,
        total_pages=total_pages,
        total_count=total_count,
    )


@orders_bp.route("/my-orders/<order_id>")
@login_required
def detail(order_id):
    """Customer order detail view with security check."""
    order = Order.find_by_id(order_id)
    if not order:
        abort(404)

    # Security: Customers can only access their own orders
    if order.user_id != current_user.id and not current_user.is_admin:
        abort(403)

    return render_template("orders/detail.html", order=order)

