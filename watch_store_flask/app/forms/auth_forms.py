from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, ValidationError
from app.models.user import User


class LoginForm(FlaskForm):
    """Login form with CSRF protection."""
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Vui lòng nhập email"),
            Email(message="Địa chỉ email không hợp lệ"),
        ],
    )
    password = PasswordField(
        "Mật khẩu",
        validators=[DataRequired(message="Vui lòng nhập mật khẩu")],
    )
    remember = BooleanField("Ghi nhớ đăng nhập")
    submit = SubmitField("Đăng nhập")


class RegisterForm(FlaskForm):
    """User registration form."""
    fullName = StringField(
        "Họ và tên",
        validators=[
            DataRequired(message="Vui lòng nhập họ và tên"),
            Length(min=2, max=100, message="Họ và tên từ 2 đến 100 ký tự"),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Vui lòng nhập email"),
            Email(message="Địa chỉ email không hợp lệ"),
        ],
    )
    password = PasswordField(
        "Mật khẩu",
        validators=[
            DataRequired(message="Vui lòng nhập mật khẩu"),
            Length(min=6, message="Mật khẩu tối thiểu 6 ký tự"),
        ],
    )
    confirm_password = PasswordField(
        "Xác nhận mật khẩu",
        validators=[
            DataRequired(message="Vui lòng xác nhận mật khẩu"),
            EqualTo("password", message="Mật khẩu xác nhận không khớp"),
        ],
    )
    phone = StringField("Số điện thoại", validators=[Optional(), Length(max=20)])
    address = TextAreaField("Địa chỉ", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Đăng ký tài khoản")

    def validate_email(self, field):
        if User.find_by_email(field.data):
            raise ValidationError("Email này đã được sử dụng. Vui lòng chọn email khác.")


class ProfileForm(FlaskForm):
    """Update profile form."""
    fullName = StringField(
        "Họ và tên",
        validators=[
            DataRequired(message="Vui lòng nhập họ và tên"),
            Length(min=2, max=100),
        ],
    )
    phone = StringField("Số điện thoại", validators=[Optional(), Length(max=20)])
    address = TextAreaField("Địa chỉ giao hàng", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Cập nhật thông tin")


class ChangePasswordForm(FlaskForm):
    """Change password form."""
    current_password = PasswordField(
        "Mật khẩu hiện tại",
        validators=[DataRequired(message="Vui lòng nhập mật khẩu hiện tại")],
    )
    new_password = PasswordField(
        "Mật khẩu mới",
        validators=[
            DataRequired(message="Vui lòng nhập mật khẩu mới"),
            Length(min=6, message="Mật khẩu mới tối thiểu 6 ký tự"),
        ],
    )
    confirm_password = PasswordField(
        "Xác nhận mật khẩu mới",
        validators=[
            DataRequired(message="Vui lòng xác nhận mật khẩu mới"),
            EqualTo("new_password", message="Mật khẩu xác nhận không khớp"),
        ],
    )
    submit = SubmitField("Đổi mật khẩu")

