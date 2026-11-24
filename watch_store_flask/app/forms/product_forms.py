from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, Length


class ProductForm(FlaskForm):
    """Admin product create/edit form."""
    name = StringField(
        "Tên sản phẩm",
        validators=[
            DataRequired(message="Vui lòng nhập tên sản phẩm"),
            Length(min=2, max=200, message="Tên sản phẩm từ 2 đến 200 ký tự"),
        ],
    )
    price = FloatField(
        "Giá bán (VNĐ)",
        validators=[
            DataRequired(message="Vui lòng nhập giá bán"),
            NumberRange(min=0, message="Giá bán phải lớn hơn hoặc bằng 0"),
        ],
    )
    brand = StringField("Thương hiệu", validators=[Optional(), Length(max=100)])
    category = StringField("Danh mục", validators=[Optional(), Length(max=100)])
    stock = IntegerField(
        "Số lượng tồn kho",
        default=10,
        validators=[
            DataRequired(message="Vui lòng nhập số lượng tồn kho"),
            NumberRange(min=0, message="Tồn kho không được âm"),
        ],
    )
    image = StringField("URL Hình ảnh", validators=[Optional(), Length(max=1000)])
    description = TextAreaField("Mô tả sản phẩm", validators=[Optional()])
    status = SelectField(
        "Trạng thái hiển thị",
        choices=[("Hiện", "Hiện"), ("Ẩn", "Ẩn")],
        default="Hiện",
    )
    submit = SubmitField("Lưu sản phẩm")


class CategoryForm(FlaskForm):
    """Admin category create/edit form."""
    name = StringField(
        "Tên danh mục",
        validators=[
            DataRequired(message="Vui lòng nhập tên danh mục"),
            Length(min=2, max=100),
        ],
    )
    group = SelectField(
        "Nhóm danh mục",
        choices=[
            ("general", "Chung"),
            ("gender", "Giới tính (Nam/Nữ/Unisex)"),
            ("brand", "Thương hiệu"),
        ],
        default="general",
    )
    description = TextAreaField("Mô tả", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Lưu danh mục")

