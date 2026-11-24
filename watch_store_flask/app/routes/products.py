from flask import Blueprint, render_template, request, abort
from app.models.product import Product
from app.models.category import Category
from app.services.network_service import NetworkService

products_bp = Blueprint("products", __name__)


@products_bp.route("/products")
def catalog():
    """Product catalog with search, category/brand filters, sorting, and pagination."""
    keyword = request.args.get("keyword", "").strip()
    category = request.args.get("category", "").strip()
    brand = request.args.get("brand", "").strip()
    sort_by = request.args.get("sort", "newest").strip()

    try:
        page = max(1, int(request.args.get("page", 1)))
    except (ValueError, TypeError):
        page = 1

    per_page = 8

    products, total_count, total_pages = Product.find_filtered_and_paginated(
        keyword=keyword if keyword else None,
        category=category if category else None,
        brand=brand if brand else None,
        sort_by=sort_by,
        page=page,
        per_page=per_page,
    )

    categories = Category.find_all()
    brands = Product.get_distinct_brands()

    # Network feature: Exchange rate (USD / VND)
    rate_info = NetworkService.get_usd_to_vnd_rate_urllib()
    rate_vnd = rate_info.get("rate_vnd", 25450.0)

    return render_template(
        "products/list.html",
        products=products,
        keyword=keyword,
        active_category=category,
        active_brand=brand,
        active_sort=sort_by,
        page=page,
        total_pages=total_pages,
        total_count=total_count,
        categories=categories,
        brands=brands,
        rate_vnd=rate_vnd,
    )


@products_bp.route("/products/<product_id>")
def detail(product_id):
    """Product detail page."""
    product = Product.find_by_id(product_id)
    if not product or product.status == "Ẩn":
        abort(404)

    # Related products
    related_products, _, _ = Product.find_filtered_and_paginated(
        category=product.category,
        per_page=4,
    )
    related = [p for p in related_products if p.id != product.id][:4]

    # USD conversion
    rate_info = NetworkService.get_usd_to_vnd_rate_urllib()
    usd_price = round(product.price / rate_info.get("rate_vnd", 25450.0), 2)

    return render_template(
        "products/detail.html",
        product=product,
        related_products=related,
        usd_price=usd_price,
    )

