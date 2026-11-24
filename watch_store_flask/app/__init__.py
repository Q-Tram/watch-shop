from datetime import datetime
from flask import Flask, render_template
from flask_login import LoginManager
from flask_mail import Mail
from app.config import config_by_name
from app.db import init_db
from app.models.user import User
from app.models.setting import Setting
from app.services.cart_service import CartService

login_manager = LoginManager()
mail = Mail()


def create_app(config_name="default"):
    """Application factory for Flask Large Application Structure."""
    app = Flask(__name__)
    config_cls = config_by_name.get(config_name, config_by_name["default"])
    app.config.from_object(config_cls)

    # Initialize MongoDB connection
    init_db(app)

    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Vui lòng đăng nhập để tiếp tục."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        return User.find_by_id(user_id)

    # Initialize Flask-Mail
    mail.init_app(app)

    # Custom Jinja2 template filters
    @app.template_filter("currency")
    def currency_filter(value):
        try:
            val = float(value or 0)
            return f"{int(val):,} đ".replace(",", ".")
        except (ValueError, TypeError):
            return "0 đ"

    @app.template_filter("datetime_format")
    def datetime_filter(value, format_str="%d/%m/%Y %H:%M"):
        if not value:
            return ""
        if isinstance(value, datetime):
            return value.strftime(format_str)
        try:
            dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
            return dt.strftime(format_str)
        except Exception:
            return str(value)

    # Context processors: inject cart count & website settings globally
    @app.context_processor
    def inject_global_data():
        try:
            cart = CartService.get_cart_details()
            cart_count = cart.get("total_quantity", 0)
        except Exception:
            cart_count = 0

        try:
            site_settings = Setting.get_website_settings()
        except Exception:
            site_settings = {}

        return {
            "cart_count": cart_count,
            "site_settings": site_settings,
            "current_year": datetime.now().year,
        }

    # Error handlers
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("errors/500.html"), 500

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.products import products_bp
    from app.routes.cart import cart_bp
    from app.routes.orders import orders_bp
    from app.routes.admin import admin_bp
    from app.routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    return app

