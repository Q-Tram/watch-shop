import logging
from flask import current_app
from flask_mail import Message

logger = logging.getLogger(__name__)


class MailService:
    """Service to handle transactional email sending with graceful fallback."""

    @classmethod
    def is_configured(cls):
        """Check if SMTP credentials are fully provided in configuration."""
        username = current_app.config.get("MAIL_USERNAME")
        password = current_app.config.get("MAIL_PASSWORD")
        server = current_app.config.get("MAIL_SERVER")
        return bool(username and password and server and username != "your_email@gmail.com")

    @classmethod
    def send_order_confirmation(cls, order, recipient_email):
        """Send order confirmation email.

        Returns (success: bool, message: str).
        """
        if not cls.is_configured():
            msg = "Chưa cấu hình tài khoản SMTP (MAIL_USERNAME/MAIL_PASSWORD) trong .env. Email xác nhận chưa được gửi đi."
            logger.info(msg)
            return False, msg

        mail_ext = current_app.extensions.get("mail")
        if not mail_ext:
            return False, "Extension Flask-Mail chưa được khởi tạo."

        try:
            subject = f"WatchStore - Xác nhận đơn hàng #{order.id[-6:].upper()}"
            items_text = "\n".join([
                f"- {it.get('name')} x {it.get('quantity')} = {int(it.get('price', 0) * it.get('quantity', 1)):,} VNĐ"
                for it in order.items
            ])

            body = f"""Xin chào {order.shippingInfo.get('fullName')},

Cảm ơn bạn đã đặt hàng tại WatchStore!

Mã đơn hàng: #{order.id}
Ngày đặt: {order.createdAt}
Phương thức thanh toán: {order.paymentMethod}
Trạng thái thanh toán: {order.paymentStatus}

Chi tiết sản phẩm:
{items_text}

Tổng giá trị đơn hàng: {int(order.totalAmount):,} VNĐ
Địa chỉ giao hàng: {order.shippingInfo.get('address')}
Số điện thoại: {order.shippingInfo.get('phone')}

Chúng tôi sẽ liên hệ và giao hàng sớm nhất có thể.
Trân trọng,
Đội ngũ WatchStore
"""
            msg = Message(
                subject=subject,
                recipients=[recipient_email],
                body=body,
            )
            mail_ext.send(msg)
            return True, f"Email xác nhận đơn hàng đã được gửi đến {recipient_email}."
        except Exception as e:
            err_msg = f"Lỗi gửi email qua máy chủ SMTP: {str(e)}"
            logger.error(err_msg)
            return False, err_msg

    @classmethod
    def send_welcome_email(cls, user):
        """Send welcome email upon registration."""
        if not cls.is_configured():
            return False, "Chưa cấu hình SMTP máy chủ. Email chào mừng chưa được gửi."

        mail_ext = current_app.extensions.get("mail")
        if not mail_ext:
            return False, "Flask-Mail chưa khởi tạo."

        try:
            msg = Message(
                subject="Chào mừng bạn đến với WatchStore",
                recipients=[user.email],
                body=f"""Xin chào {user.fullName},

Chào mừng bạn đã trở thành thành viên của WatchStore!
Tài khoản đăng nhập của bạn: {user.email}

Chúc bạn có những trải nghiệm mua sắm đồng hồ tuyệt vời tại cửa hàng của chúng tôi.

Trân trọng,
Đội ngũ WatchStore
""",
            )
            mail_ext.send(msg)
            return True, f"Email chào mừng đã được gửi đến {user.email}."
        except Exception as e:
            return False, f"Lỗi gửi email: {str(e)}"

