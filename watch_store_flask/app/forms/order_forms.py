from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, RadioField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class CheckoutForm(FlaskForm):
    """Customer checkout form."""
    fullName = StringField(
        "Họ và tên người nhận",
        validators=[
            DataRequired(message="Vui lòng nhập họ và tên người nhận"),
            Length(min=2, max=100),
        ],
    )
    phone = StringField(
        "Số điện thoại nhận hàng",
        validators=[
            DataRequired(message="Vui lòng nhập số điện thoại nhận hàng"),
            Length(min=8, max=20, message="Số điện thoại từ 8 đến 20 số"),
        ],
    )
    address = TextAreaField(
        "Địa chỉ giao hàng chi tiết",
        validators=[
            DataRequired(message="Vui lòng nhập địa chỉ giao hàng"),
            Length(min=5, max=300),
        ],
    )
    note = TextAreaField("Ghi chú đơn hàng (nếu có)", validators=[Optional(), Length(max=300)])
    paymentMethod = RadioField(
        "Phương thức thanh toán",
        choices=[
            ("COD", "Thanh toán khi nhận hàng (COD)"),
            ("QR", "Thanh toán chuyển khoản qua mã QR"),
        ],
        default="COD",
        validators=[DataRequired(message="Vui lòng chọn phương thức thanh toán")],
    )
    submit = SubmitField("Xác nhận đặt hàng")


class OrderStatusForm(FlaskForm):
    """Admin order update form."""
    orderStatus = SelectField(
        "Trạng thái đơn hàng",
        choices=[
            ("pending", "Chờ xác nhận"),
            ("confirmed", "Đã xác nhận"),
            ("shipping", "Đang giao"),
            ("delivered", "Đã giao"),
            ("cancelled", "Đã hủy"),
        ],
        validators=[DataRequired()],
    )
    paymentStatus = SelectField(
        "Trạng thái thanh toán",
        choices=[
            ("unpaid", "Chưa thanh toán"),
            ("paid", "Đã thanh toán"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Cập nhật đơn hàng")

