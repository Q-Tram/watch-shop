from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user


def admin_required(f):
    """Decorator to restrict access to administrator accounts only."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Vui lòng đăng nhập với quyền quản trị viên.", "warning")
            return redirect(url_for("auth.login"))
        if not getattr(current_user, "is_admin", False):
            flash("Bạn không có quyền truy cập khu vực quản trị.", "danger")
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

