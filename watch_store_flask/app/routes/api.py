from flask import Blueprint, jsonify, request
from app.models.product import Product
from app.models.order import Order
from app.services.network_service import NetworkService

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")


@api_bp.route("/products", methods=["GET"])
def get_products():
    """Internal REST API: Get paginated products."""
    keyword = request.args.get("keyword")
    category = request.args.get("category")
    brand = request.args.get("brand")

    try:
        page = max(1, int(request.args.get("page", 1)))
        per_page = min(50, max(1, int(request.args.get("limit", 10))))
    except (ValueError, TypeError):
        page = 1
        per_page = 10

    products, total, total_pages = Product.find_filtered_and_paginated(
        keyword=keyword,
        category=category,
        brand=brand,
        page=page,
        per_page=per_page,
    )

    return jsonify({
        "status": "success",
        "data": [p.to_dict() for p in products],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_items": total,
            "total_pages": total_pages,
        },
    })


@api_bp.route("/products/<product_id>", methods=["GET"])
def get_product(product_id):
    """Internal REST API: Get product by ID."""
    product = Product.find_by_id(product_id)
    if not product:
        return jsonify({"status": "error", "message": "Product not found"}), 404

    return jsonify({"status": "success", "data": product.to_dict()})


@api_bp.route("/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    """Internal REST API: Get order details."""
    order = Order.find_by_id(order_id)
    if not order:
        return jsonify({"status": "error", "message": "Order not found"}), 404

    return jsonify({"status": "success", "data": order.to_dict()})


@api_bp.route("/stats", methods=["GET"])
def get_stats():
    """Internal REST API: Get business metrics."""
    stats = Order.get_dashboard_stats()
    return jsonify({
        "status": "success",
        "data": {
            "total_revenue": stats["total_revenue"],
            "total_orders": stats["total_orders"],
            "total_customers": stats["total_customers"],
            "total_products": stats["total_products"],
            "status_counts": stats["status_counts"],
        },
    })


@api_bp.route("/exchange-rate", methods=["GET"])
def get_exchange_rate():
    """Network integration API: Fetches USD/VND exchange rate via urllib."""
    rate_info = NetworkService.get_usd_to_vnd_rate_urllib()
    return jsonify({"status": "success", "data": rate_info})


@api_bp.route("/banks", methods=["GET"])
def get_banks():
    """Network integration API: Fetches supported Vietnamese banks via requests."""
    banks_info = NetworkService.get_supported_banks_requests()
    return jsonify({"status": "success", "data": banks_info})

