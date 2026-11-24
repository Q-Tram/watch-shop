from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, Email


class WebsiteSettingForm(FlaskForm):
    """Admin website settings form."""
    siteName = StringField("Tên website", validators=[DataRequired(), Length(max=100)])
    footerDescription = TextAreaField("Mô tả chân trang", validators=[Optional(), Length(max=500)])
    logoUrl = StringField("URL Logo", validators=[Optional(), Length(max=1000)])
    contactEmail = StringField("Email liên hệ", validators=[Optional(), Email(), Length(max=100)])
    contactPhone = StringField("Điện thoại liên hệ", validators=[Optional(), Length(max=50)])
    contactAddress = StringField("Địa chỉ cửa hàng", validators=[Optional(), Length(max=255)])
    workingHours = StringField("Giờ làm việc", validators=[Optional(), Length(max=100)])
    contactSlogan = StringField("Slogan thương hiệu", validators=[Optional(), Length(max=100)])
    facebookUrl = StringField("Facebook URL", validators=[Optional(), Length(max=500)])
    instagramUrl = StringField("Instagram URL", validators=[Optional(), Length(max=500)])
    tiktokUrl = StringField("TikTok URL", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Lưu cài đặt website")


class PaymentSettingForm(FlaskForm):
    """Admin payment and QR settings form."""
    bankName = StringField("Tên ngân hàng", validators=[DataRequired(), Length(max=100)])
    accountNumber = StringField("Số tài khoản", validators=[DataRequired(), Length(max=50)])
    accountName = StringField("Tên chủ tài khoản", validators=[DataRequired(), Length(max=100)])
    transferContent = StringField("Nội dung chuyển khoản mặc định", validators=[DataRequired(), Length(max=200)])
    isQrEnabled = BooleanField("Bật thanh toán bằng mã QR")
    qrImage = StringField("URL Hình ảnh QR tĩnh (tùy chọn)", validators=[Optional(), Length(max=1000)])
    submit = SubmitField("Lưu cấu hình thanh toán")

