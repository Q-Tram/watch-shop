from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from app.utils.decorators import admin_required
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order, ORDER_STATUSES
from app.models.user import User
from app.models.setting import Setting
from app.forms.product_forms import ProductForm, CategoryForm
from app.forms.order_forms import OrderStatusForm
from app.forms.setting_forms import WebsiteSettingForm, PaymentSettingForm

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    """Admin dashboard with overview metrics and recent records."""
    stats = Order.get_dashboard_stats()
    recent_products, _, _ = Product.find_filtered_and_paginated(status=None, per_page=5)
    recent_customers, _, _ = User.get_all_customers(per_page=5)

    return render_template(
        "admin/dashboard.html",
        stats=stats,
        recent_products=recent_products,
        recent_customers=recent_customers,
    )


# ==========================================
# PRODUCT MANAGEMENT (CRUD)
# ==========================================
@admin_bp.route("/products")
@admin_required
def products():
    keyword = request.args.get("keyword", "").strip()
    category = request.args.get("category", "").strip()
    status = request.args.get("status", "").strip()

    try:
        page = max(1, int(request.args.get("page", 1)))
    except (ValueError, TypeError):
        page = 1

    products_list, total_count, total_pages = Product.find_filtered_and_paginated(
        keyword=keyword if keyword else None,
        category=category if category else None,
        status=status if status else None,
        page=page,
        per_page=10,
    )
    categories_list = Category.find_all()

    return render_template(
        "admin/products/list.html",
        products=products_list,
        keyword=keyword,
        active_category=category,
        active_status=status,
        page=page,
        total_pages=total_pages,
        total_count=total_count,
        categories=categories_list,
    )


@admin_bp.route("/products/new", methods=["GET", "POST"])
@admin_required
def product_create():
    form = ProductForm()
    if form.validate_on_submit():
        Product.create(
            name=form.name.data,
            price=form.price.data,
            brand=form.brand.data,
            category=form.category.data,
            stock=form.stock.data,
            image=form.image.data,
            description=form.description.data,
            status=form.status.data,
        )
        flash("Thêm mới sản phẩm thành công!", "success")
        return redirect(url_for("admin.products"))

    return render_template("admin/products/form.html", form=form, title="Thêm mới sản phẩm")


@admin_bp.route("/products/<product_id>/edit", methods=["GET", "POST"])
@admin_required
def product_edit(product_id):
    product = Product.find_by_id(product_id)
    if not product:
        abort(404)

    form = ProductForm(
        name=product.name,
        price=product.price,
        brand=product.brand,
        category=product.category,
        stock=product.stock,
        image=product.image,
        description=product.description,
        status=product.status,
    )

    if form.validate_on_submit():
        Product.update(
            product_id=product.id,
            name=form.name.data,
            price=form.price.data,
            brand=form.brand.data,
            category=form.category.data,
            stock=form.stock.data,
            image=form.image.data,
            description=form.description.data,
            status=form.status.data,
        )
        flash("Cập nhật thông tin sản phẩm thành công!", "success")
        return redirect(url_for("admin.products"))

    return render_template("admin/products/form.html", form=form, title="Chỉnh sửa sản phẩm", product=product)


@admin_bp.route("/products/<product_id>/delete", methods=["POST"])
@admin_required
def product_delete(product_id):
    Product.delete(product_id)
    flash("Đã xóa sản phẩm thành công.", "info")
    return redirect(url_for("admin.products"))


@admin_bp.route("/products/<product_id>/toggle-status", methods=["POST"])
@admin_required
def product_toggle_status(product_id):
    product = Product.find_by_id(product_id)
    if not product:
        abort(404)
    new_status = "Ẩn" if product.status == "Hiện" else "Hiện"
    Product.update(
        product_id=product.id,
        name=product.name,
        price=product.price,
        brand=product.brand,
        category=product.category,
        stock=product.stock,
        image=product.image,
        description=product.description,
        status=new_status,
    )
    flash(f"Đã chuyển trạng thái sản phẩm sang '{new_status}'.", "success")
    return redirect(url_for("admin.products"))


# ==========================================
# CATEGORY MANAGEMENT (CRUD)
# ==========================================
@admin_bp.route("/categories")
@admin_required
def categories():
    categories_list = Category.find_all()
    return render_template("admin/categories/list.html", categories=categories_list)


@admin_bp.route("/categories/new", methods=["GET", "POST"])
@admin_required
def category_create():
    form = CategoryForm()
    if form.validate_on_submit():
        Category.create(
            name=form.name.data,
            description=form.description.data,
            group=form.group.data,
        )
        flash("Thêm mới danh mục thành công!", "success")
        return redirect(url_for("admin.categories"))

    return render_template("admin/categories/form.html", form=form, title="Thêm danh mục mới")


@admin_bp.route("/categories/<category_id>/edit", methods=["GET", "POST"])
@admin_required
def category_edit(category_id):
    cat = Category.find_by_id(category_id)
    if not cat:
        abort(404)

    form = CategoryForm(
        name=cat.name,
        group=cat.group,
        description=cat.description,
    )

    if form.validate_on_submit():
        Category.update(
            category_id=cat.id,
            name=form.name.data,
            description=form.description.data,
            group=form.group.data,
        )
        flash("Cập nhật danh mục thành công!", "success")
        return redirect(url_for("admin.categories"))

    return render_template("admin/categories/form.html", form=form, title="Chỉnh sửa danh mục", category=cat)


@admin_bp.route("/categories/<category_id>/delete", methods=["POST"])
@admin_required
def category_delete(category_id):
    Category.delete(category_id)
    flash("Đã xóa danh mục.", "info")
    return redirect(url_for("admin.categories"))


# ==========================================
# ORDER MANAGEMENT
# ==========================================
@admin_bp.route("/orders")
@admin_required
def orders():
    status = request.args.get("status", "").strip()
    search = request.args.get("search", "").strip()
    try:
        page = max(1, int(request.args.get("page", 1)))
    except (ValueError, TypeError):
        page = 1

    orders_list, total_count, total_pages = Order.find_all_paginated(
        status=status if status else None,
        search=search if search else None,
        page=page,
        per_page=10,
    )

    return render_template(
        "admin/orders/list.html",
        orders=orders_list,
        active_status=status,
        search=search,
        page=page,
        total_pages=total_pages,
        total_count=total_count,
        statuses=ORDER_STATUSES,
    )


@admin_bp.route("/orders/<order_id>", methods=["GET", "POST"])
@admin_required
def order_detail(order_id):
    order = Order.find_by_id(order_id)
    if not order:
        abort(404)

    form = OrderStatusForm(
        orderStatus=order.orderStatus,
        paymentStatus=order.paymentStatus,
    )

    if form.validate_on_submit():
        Order.update_status(order.id, form.orderStatus.data)
        Order.update_payment_status(order.id, form.paymentStatus.data)
        flash("Cập nhật trạng thái đơn hàng thành công!", "success")
        return redirect(url_for("admin.order_detail", order_id=order.id))

    return render_template("admin/orders/detail.html", order=order, form=form)


# ==========================================
# CUSTOMER MANAGEMENT
# ==========================================
@admin_bp.route("/customers")
@admin_required
def customers():
    search = request.args.get("search", "").strip()
    try:
        page = max(1, int(request.args.get("page", 1)))
    except (ValueError, TypeError):
        page = 1

    customers_list, total_count, total_pages = User.get_all_customers(
        search=search if search else None,
        page=page,
        per_page=10,
    )

    return render_template(
        "admin/customers/list.html",
        customers=customers_list,
        search=search,
        page=page,
        total_pages=total_pages,
        total_count=total_count,
    )


@admin_bp.route("/customers/<customer_id>/toggle-lock", methods=["POST"])
@admin_required
def customer_toggle_lock(customer_id):
    user = User.toggle_lock(customer_id)
    if not user:
        abort(404)
    action = "Mở khóa" if user.isActive else "Khóa"
    flash(f"Đã {action} tài khoản khách hàng '{user.fullName}'.", "info")
    return redirect(url_for("admin.customers"))


# ==========================================
# WEBSITE & PAYMENT SETTINGS
# ==========================================
@admin_bp.route("/settings", methods=["GET", "POST"])
@admin_required
def settings():
    ws_doc = Setting.get_website_settings()
    ps_doc = Setting.get_payment_settings()

    ws_form = WebsiteSettingForm(prefix="ws", **ws_doc)
    ps_form = PaymentSettingForm(prefix="ps", **ps_doc)

    if request.method == "POST":
        action = request.form.get("form_action")
        if action == "website" and ws_form.validate_on_submit():
            Setting.update_website_settings(ws_form.data)
            flash("Đã lưu cài đặt website thành công!", "success")
            return redirect(url_for("admin.settings"))
        elif action == "payment" and ps_form.validate_on_submit():
            Setting.update_payment_settings(ps_form.data)
            flash("Đã lưu cấu hình thanh toán và mã QR thành công!", "success")
            return redirect(url_for("admin.settings"))

    return render_template(
        "admin/settings/index.html",
        ws_form=ws_form,
        ps_form=ps_form,
        ps_doc=ps_doc,
    )

