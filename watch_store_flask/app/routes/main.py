from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models.product import Product
from app.models.setting import Setting

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Home page."""
    featured_products = Product.get_featured(limit=8)
    settings = Setting.get_website_settings()
    return render_template(
        "main/index.html",
        featured_products=featured_products,
        settings=settings,
    )


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    """Contact page."""
    settings = Setting.get_website_settings()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if not name or not email or not message:
            flash("Vui lòng nhập đầy đủ họ tên, email và nội dung liên hệ.", "danger")
        else:
            flash("Cảm ơn bạn đã liên hệ! Đội ngũ WatchStore sẽ phản hồi sớm nhất có thể.", "success")
            return redirect(url_for("main.contact"))

    return render_template("main/contact.html", settings=settings)

