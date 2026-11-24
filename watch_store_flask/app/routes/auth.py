from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms.auth_forms import LoginForm, RegisterForm, ProfileForm, ChangePasswordForm
from app.models.user import User
from app.services.mail_service import MailService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_email(form.email.data)
        if not user:
            flash("Email không tồn tại trong hệ thống.", "danger")
        elif not user.isActive:
            flash("Tài khoản của bạn đã bị khóa. Vui lòng liên hệ quản trị viên.", "danger")
        elif not user.check_password(form.password.data):
            flash("Mật khẩu không chính xác. Vui lòng thử lại.", "danger")
        else:
            login_user(user, remember=form.remember.data)
            flash(f"Đăng nhập thành công! Xin chào {user.fullName}.", "success")
            next_page = request.args.get("next")
            if next_page and next_page.startswith("/"):
                return redirect(next_page)
            if user.is_admin:
                return redirect(url_for("admin.dashboard"))
            return redirect(url_for("main.index"))

    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User.create(
            fullName=form.fullName.data,
            email=form.email.data,
            password=form.password.data,
            phone=form.phone.data or "",
            address=form.address.data or "",
            role="customer",
        )
        # Attempt welcome email
        mail_sent, mail_msg = MailService.send_welcome_email(user)
        if mail_sent:
            flash(f"Đăng ký thành công! {mail_msg} Vui lòng đăng nhập.", "success")
        else:
            flash("Đăng ký tài khoản thành công! Vui lòng đăng nhập.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Bạn đã đăng xuất an toàn.", "info")
    return redirect(url_for("main.index"))


@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm(
        fullName=current_user.fullName,
        phone=current_user.phone,
        address=current_user.address,
    )
    if form.validate_on_submit():
        User.update_profile(
            user_id=current_user.id,
            full_name=form.fullName.data,
            phone=form.phone.data,
            address=form.address.data,
        )
        flash("Cập nhật thông tin cá nhân thành công!", "success")
        return redirect(url_for("auth.profile"))

    return render_template("auth/profile.html", form=form)


@auth_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash("Mật khẩu hiện tại không đúng.", "danger")
        else:
            User.change_password(current_user.id, form.new_password.data)
            flash("Đổi mật khẩu thành công! Vui lòng sử dụng mật khẩu mới cho lần đăng nhập sau.", "success")
            return redirect(url_for("auth.profile"))

    return render_template("auth/change_password.html", form=form)

