# WatchStore - Hệ Thống Website Bán Đồng Hồ Trực Tuyến
### Đồ án môn học: Lập trình Python nâng cao (Flask & MongoDB)

Dự án website thương mại điện tử chuyên kinh doanh đồng hồ chính hãng cao cấp, được xây dựng hoàn chỉnh trên nền tảng **Python / Flask** và cơ sở dữ liệu NoSQL **MongoDB**. Ứng dụng tái hiện đầy đủ luồng nghiệp vụ và chức năng của dự án tham khảo gốc, đồng thời tuân thủ toàn diện các chuẩn mực kiến trúc Flask Large Application Structure và mẫu báo cáo đồ án.

---

## 1. CÔNG NGHỆ SỬ DỤNG
- **Ngôn ngữ & Framework:** Python 3.13, Flask 3.1.0
- **Giao diện người dùng (GUI Web):** Jinja2 Templates, Bootstrap 5.3, HTML5, CSS3, JavaScript. Giao diện thiết kế theo phong cách Luxury Dark/Gold, chuẩn Responsive tương thích điện thoại, máy tính bảng và màn hình máy tính.
- **Xử lý Form & Bảo mật:** Flask-WTF, WTForms, CSRF Protection, chống tấn công XSS và SQL/NoSQL Injection.
- **Cơ sở dữ liệu:** MongoDB (sử dụng PyMongo và fallback tự động mongomock khi chạy độc lập kiểm thử), cơ chế lập chỉ mục (Indexing) và phân trang trực tiếp ở tầng dữ liệu.
- **Xác thực & Phân quyền:** Flask-Login, mã hóa mật khẩu an toàn bằng Scrypt/Werkzeug (không lưu plain text), phân quyền 2 cấp độ: Khách hàng (`customer`) và Quản trị viên (`admin`).
- **Gửi Email giao dịch:** Flask-Mail (cấu hình SMTP qua biến môi trường, có cơ chế kiểm tra và thông báo rõ ràng khi chưa có thông tin SMTP).
- **Lập trình mạng (CLO3):**
  - Tích hợp API tỷ giá ngoại tệ trực tuyến qua `urllib.request` để quy đổi giá đồng hồ từ VNĐ sang USD theo thời gian thực.
  - Tích hợp API ngân hàng VietQR qua thư viện `requests` phục vụ cấu hình cổng thanh toán chuyển khoản và tạo mã QR động.
  - Bộ API JSON nội bộ chuẩn RESTful (`/api/v1/products`, `/api/v1/orders`, `/api/v1/stats`, `/api/v1/exchange-rate`).

---

## 2. CẤU TRÚC THƯ MỤC DỰ ÁN (Flask Large Application Structure)

```text
watch_store_flask/
├── app/
│   ├── __init__.py             # Application Factory (create_app), Jinja filters, context processors
│   ├── config.py               # Cấu hình môi trường (Development, Testing, Production)
│   ├── db.py                   # Kết nối MongoDB (PyMongo + mongomock fallback, tạo indexes)
│   ├── models/                 # Lớp thực thể dữ liệu & Repositories MongoDB
│   │   ├── __init__.py
│   │   ├── user.py             # User model (UserMixin, role, password hash, status lock)
│   │   ├── category.py         # Category model (slug generator, group)
│   │   ├── product.py          # Product model (search, filter, pagination, stock decrement)
│   │   ├── order.py            # Order model (item snapshot, status, revenue statistics)
│   │   └── setting.py          # Setting & PaymentSetting models (brand info, VietQR config)
│   ├── forms/                  # Lớp Web Forms (Flask-WTF & CSRF)
│   │   ├── __init__.py
│   │   ├── auth_forms.py       # Login, Register, Profile, ChangePassword forms
│   │   ├── product_forms.py    # Product & Category CRUD forms
│   │   ├── order_forms.py      # Checkout & OrderStatus update forms
│   │   └── setting_forms.py    # Website & Payment settings forms
│   ├── services/               # Tầng xử lý nghiệp vụ (Business Logic)
│   │   ├── __init__.py
│   │   ├── cart_service.py     # Giỏ hàng Session, kiểm tra tồn kho realtime
│   │   ├── order_service.py    # Quy trình đặt hàng, trừ tồn kho nguyên tử, tạo snapshot
│   │   ├── mail_service.py     # Gửi email xác nhận đơn hàng qua Flask-Mail
│   │   └── network_service.py  # Lập trình mạng urllib / requests gọi API ngoài
│   ├── utils/                  # Tiện ích & Middleware
│   │   ├── __init__.py
│   │   └── decorators.py       # Decorator @admin_required kiểm soát quyền quản trị
│   ├── routes/                 # Blueprints định tuyến
│   │   ├── __init__.py
│   │   ├── main.py             # Trang chủ, liên hệ
│   │   ├── auth.py             # Đăng ký, đăng nhập, đăng xuất, hồ sơ
│   │   ├── products.py         # Danh mục, tìm kiếm, lọc, phân trang, chi tiết
│   │   ├── cart.py             # Thêm, sửa số lượng, xóa sản phẩm, làm trống giỏ
│   │   ├── orders.py           # Thanh toán COD/QR, chi tiết đơn, lịch sử đơn hàng
│   │   ├── admin.py            # Dashboard thống kê, CRUD SP/DM, quản lý đơn, khách hàng, settings
│   │   └── api.py              # RESTful API endpoints & proxy mạng
│   ├── templates/              # Giao diện Jinja2 kế thừa
│   │   ├── base.html           # Template gốc (Navbar, Flash alerts, Footer)
│   │   ├── errors/             # Trang lỗi 403, 404, 500
│   │   ├── main/               # index.html, contact.html
│   │   ├── auth/               # login.html, register.html, profile.html, change_password.html
│   │   ├── products/           # list.html, detail.html
│   │   ├── cart/               # index.html
│   │   ├── orders/             # checkout.html, success.html, list.html, detail.html
│   │   └── admin/              # layout.html, dashboard.html, products/, categories/, orders/, customers/, settings/
│   └── static/                 # Tài nguyên tĩnh
│       ├── css/style.css       # Tùy biến phong cách Luxury Watch Dark/Gold
│       └── js/main.js          # Xử lý tương tác client, tự động đóng alert
├── tests/                      # Bộ kiểm thử tự động (Pytest)
│   ├── conftest.py             # Fixtures, test app client, database reset
│   ├── test_auth.py            # Test đăng ký, đăng nhập, hash mật khẩu, khóa tài khoản
│   ├── test_products.py        # Test tìm kiếm, lọc danh mục, phân trang, chi tiết SP
│   ├── test_cart_order.py      # Test giỏ hàng, đặt hàng, trừ tồn kho, bảo vệ đơn hàng
│   ├── test_admin.py           # Test phân quyền admin 403, CRUD SP/DM, khóa khách hàng
│   └── test_network_api.py     # Test API JSON nội bộ và API mạng urllib/requests
├── .env.example                # Mẫu biến môi trường giả lập (không chứa thông tin nhạy cảm)
├── requirements.txt            # Danh sách gói phụ thuộc Python
├── seed.py                     # Script nạp dữ liệu mẫu đồng hồ & tài khoản demo
├── run.py                      # File khởi động ứng dụng Flask
└── README.md
```

---

## 3. HƯỚNG DẪN CÀI ĐẶT VÀ KHỞI CHẠY TỪ ĐẦU

### Bước 1: Mở Terminal tại thư mục dự án
```bash
cd d:\watch-shop-feature-checkout-auth\watch_store_flask
```

### Bước 2: Tạo và kích hoạt môi trường ảo (Virtual Environment)
```bash
# Trên Windows PowerShell:
python -m venv venv
.\venv\Scripts\Activate.ps1

# Trên Linux/macOS:
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài đặt các gói phụ thuộc
```bash
pip install -r requirements.txt
```

### Bước 4: Thiết lập biến môi trường
Tạo file `.env` từ file mẫu `.env.example`:
```bash
cp .env.example .env
```
Nội dung `.env`:
- `MONGO_URI=mongodb://localhost:27017/watch_store` (Nếu có máy chủ MongoDB đang chạy).
- `USE_MONGOMOCK=False` (Nếu chưa cài đặt MongoDB local, hệ thống tự động sử dụng `mongomock` in-memory).
- Cấu hình SMTP (tùy chọn để gửi email thật qua Gmail App Password):
  ```env
  MAIL_SERVER=smtp.gmail.com
  MAIL_PORT=587
  MAIL_USE_TLS=True
  MAIL_USERNAME=your_email@gmail.com
  MAIL_PASSWORD=your_app_password
  ```

### Bước 5: Nạp dữ liệu mẫu (Seed Data)
Chạy script seed để tạo danh mục, 12 mẫu đồng hồ cao cấp, cấu hình website/QR và 2 tài khoản demo:
```bash
python seed.py
```

### Bước 6: Khởi chạy website
```bash
python run.py
```
Mở trình duyệt web và truy cập địa chỉ: **`http://127.0.0.1:5000`**

---

## 4. TÀI KHOẢN TRẢI NGHIỆM DEMO (CHỈ DÙNG LOCAL)

| Phân quyền | Email đăng nhập | Mật khẩu | Mục đích sử dụng |
| :--- | :--- | :--- | :--- |
| **Quản trị viên (Admin)** | `admin@gmail.com` | `123456` | Truy cập `/admin`, xem Dashboard thống kê doanh thu, CRUD sản phẩm & danh mục, xử lý trạng thái đơn hàng, khóa/mở tài khoản khách hàng, cấu hình QR thanh toán. |
| **Khách hàng (Customer)** | `khachhang@gmail.com` | `123456` | Mua hàng, xem chi tiết, thêm giỏ, đặt hàng thanh toán COD hoặc quét mã QR chuyển khoản, xem lịch sử đơn hàng của chính mình. |

---

## 5. CHẠY BỘ KIỂM THỬ TỰ ĐỘNG (AUTOMATED TEST SUITE)
Chạy toàn bộ 23 bài kiểm thử đơn vị & tích hợp (Unit & Integration Tests) bằng Pytest:
```bash
python -m pytest tests -v
```
Kết quả mong đợi: **23 passed, 100% thành công**.

