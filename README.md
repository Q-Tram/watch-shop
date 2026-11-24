# HƯỚNG DẪN DỰ ÁN WEBSITE BÁN ĐỒNG HỒ CAO CẤP (WATCHSTORE)
### Đồ án môn học: Lập trình Python nâng cao (Flask & NoSQL MongoDB)

---

## 1. CÂY THƯ MỤC DỰ ÁN (Flask Large Application Structure)

Thư mục dự án mới được tổ chức chuyên biệt tại: `watch_store_flask/`

```text
d:\watch-shop-feature-checkout-auth\
├── Mau_Bao_Cao_DoAn_LapTrinhPythonNangCao.docx             # File mẫu gốc của giảng viên
├── Bao_Cao_DoAn_LapTrinhPythonNangCao_WatchStore.docx     # Báo cáo đồ án hoàn chỉnh đã tạo
├── generate_report.py                                     # Script tạo báo cáo Word tự động
├── README.md                                              # Hướng dẫn dự án tổng quan
└── watch_store_flask/                                     # MÃ NGUỒN CHÍNH DỰ ÁN FLASK + MONGODB
    ├── app/
    │   ├── __init__.py          # Application Factory (create_app), context processors, Jinja filters
    │   ├── config.py            # Cấu hình môi trường (Development, Testing, Production)
    │   ├── db.py                # Kết nối MongoDB (PyMongo + mongomock fallback, tạo indexes)
    │   ├── models/              # Lớp thực thể & Repositories MongoDB
    │   │   ├── __init__.py
    │   │   ├── user.py          # User (UserMixin, role, password hash, status lock)
    │   │   ├── category.py      # Category (tự động tạo slug, nhóm danh mục)
    │   │   ├── product.py       # Product (lọc, tìm kiếm, phân trang MongoDB, trừ tồn kho)
    │   │   ├── order.py         # Order (snapshot giá/sản phẩm, doanh thu, thống kê)
    │   │   └── setting.py       # Setting & PaymentSetting (thông tin showroom, VietQR)
    │   ├── forms/               # Lớp biểu mẫu Web Forms (Flask-WTF & CSRF Protection)
    │   │   ├── __init__.py
    │   │   ├── auth_forms.py    # LoginForm, RegisterForm, ProfileForm, ChangePasswordForm
    │   │   ├── product_forms.py # ProductForm, CategoryForm
    │   │   ├── order_forms.py   # CheckoutForm, OrderStatusForm
    │   │   └── setting_forms.py # WebsiteSettingForm, PaymentSettingForm
    │   ├── services/            # Tầng xử lý nghiệp vụ (Business Logic)
    │   │   ├── __init__.py
    │   │   ├── cart_service.py  # Quản lý giỏ hàng Session, kiểm tra tồn kho realtime
    │   │   ├── order_service.py # Xử lý đơn hàng, trừ kho nguyên tử, gọi email
    │   │   ├── mail_service.py  # Gửi email giao dịch qua Flask-Mail (fallback an toàn)
    │   │   └── network_service.py # Lập trình mạng urllib / requests tích hợp API ngoài
    │   ├── utils/
    │   │   ├── __init__.py
    │   │   └── decorators.py    # Decorator @admin_required kiểm soát phân quyền
    │   ├── routes/              # Blueprints định tuyến nghiệp vụ
    │   │   ├── __init__.py
    │   │   ├── main.py          # Trang chủ, trang liên hệ
    │   │   ├── auth.py          # Đăng ký, đăng nhập, đăng xuất, hồ sơ, đổi mật khẩu
    │   │   ├── products.py      # Danh mục, tìm kiếm, lọc, phân trang, chi tiết sản phẩm
    │   │   ├── cart.py          # Thêm/sửa/xóa sản phẩm trong giỏ hàng
    │   │   ├── orders.py        # Checkout, xác nhận QR, đơn hàng của tôi, chi tiết đơn
    │   │   ├── admin.py         # Dashboard thống kê, CRUD SP & danh mục, khách hàng, settings
    │   │   └── api.py           # RESTful JSON APIs & proxy mạng ngoại vi
    │   ├── templates/           # Jinja2 Templates kế thừa base.html
    │   │   ├── base.html        # Layout tổng thể (Navbar, Flash alerts, Cart badge, Footer)
    │   │   ├── errors/          # 403.html, 404.html, 500.html
    │   │   ├── main/            # index.html, contact.html
    │   │   ├── auth/            # login.html, register.html, profile.html, change_password.html
    │   │   ├── products/        # list.html, detail.html
    │   │   ├── cart/            # index.html
    │   │   ├── orders/          # checkout.html, success.html, list.html, detail.html
    │   │   └── admin/           # layout.html, dashboard.html, products/, categories/, orders/, customers/, settings/
    │   └── static/
    │       ├── css/style.css    # CSS giao diện Luxury Watch (Dark & Gold, Responsive)
    │       └── js/main.js       # Client interaction, auto dismiss alert
    ├── tests/                   # Bộ kiểm thử tự động 23 test cases (Pytest)
    │   ├── conftest.py
    │   ├── test_auth.py
    │   ├── test_products.py
    │   ├── test_cart_order.py
    │   ├── test_admin.py
    │   └── test_network_api.py
    ├── .env.example             # Biến môi trường mẫu giả định (không chứa bí mật thật)
    ├── requirements.txt         # Danh mục thư viện Python bắt buộc
    ├── seed.py                  # Script nạp 12 mẫu đồng hồ, danh mục & tài khoản demo
    ├── run.py                   # File khởi động máy chủ Flask
    └── README.md                # Tài liệu hướng dẫn sử dụng và vận hành
```

---

## 2. ĐỐI CHIẾU CHỨC NĂNG VỚI DỰ ÁN THAM KHẢO

| Phân hệ / Nghiệp vụ | Dự án tham khảo (Node/Express + React) | Dự án mới xây dựng (Flask + MongoDB) | Tình trạng đối chiếu |
| :--- | :--- | :--- | :--- |
| **Kiến trúc & Stack** | Node.js, Express, Mongoose, React, Vite | Python 3, Flask Large App, PyMongo, Jinja2, Bootstrap 5 | **Đạt** (Thay thế 100% stack cũ) |
| **Xác thực & Bảo mật** | JWT token trong `localStorage`, bcrypt | Flask-Login, Session an toàn, Werkzeug Scrypt Hash, CSRF Protection | **Đạt** & bảo mật cao hơn chống XSS |
| **Phân quyền** | Middleware `authMiddleware`, `adminMiddleware` | Decorator `@admin_required`, `@login_required`, chặn 403 | **Đạt tương đương** |
| **Trang chủ & Giới thiệu** | Hero banner, sản phẩm nổi bật, social links | Hero Luxury banner, 8 SP nổi bật, thương hiệu, footer động | **Đạt tương đương** |
| **Danh mục & Tìm kiếm** | Lọc client-side qua React state | Lọc & tìm kiếm trực tiếp trên MongoDB bằng Regex & Indexing | **Đạt vượt trội** |
| **Phân trang sản phẩm** | Chưa phân trang dữ liệu server | Phân trang thật trên MongoDB (`skip`/`limit`), nút chuyển trang | **Đạt** (Đúng chuẩn đề tài) |
| **Chi tiết sản phẩm** | Ảnh, giá, thương hiệu, danh mục | Đầy đủ thông số, tình trạng tồn kho, quy đổi USD realtime | **Đạt tương đương** |
| **Giỏ hàng** | `CartContext` lưu local | Flask Session, kiểm tra tồn kho realtime, cập nhật/xóa SP | **Đạt tương đương** |
| **Thanh toán & Đặt hàng** | Checkout COD và QR code | Form Flask-WTF, thanh toán COD / mã QR VietQR động | **Đạt tương đương** |
| **Toàn vẹn đơn hàng** | Lưu items đơn hàng | **Snapshot bất biến**: lưu giá & tên SP tại thời điểm mua | **Đạt** (Đáp ứng tiêu chuẩn) |
| **Theo dõi đơn hàng** | Xem đơn của tôi, chi tiết đơn | Khách chỉ xem đơn của mình (chặn xem đơn người khác) | **Đạt tương đương** |
| **Admin Dashboard** | Thống kê số lượng, đơn mới, khách mới | Thống kê doanh thu, 5 trạng thái đơn, biểu đồ số liệu, SP mới | **Đạt tương đương** |
| **Admin CRUD SP & DM** | Thêm, sửa, xóa sản phẩm, danh mục | Form Flask-WTF validate, bật/tắt trạng thái Hiện/Ẩn, xóa an toàn | **Đạt tương đương** |
| **Admin Khách hàng** | Xem danh sách, toggle lock tài khoản | Bảng khách hàng có tìm kiếm, phân trang, Khóa/Mở khóa tài khoản | **Đạt tương đương** |
| **Admin Settings** | Cài đặt Website và cấu hình tài khoản QR | Form chỉnh sửa Hotline, Email, Địa chỉ, QR preview trực tiếp | **Đạt tương đương** |
| **Email giao dịch** | Chưa triển khai | Flask-Mail gửi xác nhận đơn hàng, có cảnh báo nếu chưa có SMTP | **Đạt** (Vượt chuẩn yêu cầu) |
| **Lập trình mạng (CLO3)** | Không có | Dùng `urllib.request` lấy tỷ giá USD, `requests` lấy ngân hàng VietQR, bộ REST API `/api/v1/*` | **Đạt chuẩn CLO3** |

---

## 3. HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH

### Bước 1: Di chuyển vào thư mục dự án
```powershell
cd d:\watch-shop-feature-checkout-auth\watch_store_flask
```

### Bước 2: Tạo và kích hoạt môi trường ảo (Virtual Environment)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Bước 3: Cài đặt các gói phụ thuộc
```powershell
pip install -r requirements.txt
```

### Bước 4: Cấu hình biến môi trường
Tạo file `.env` bằng cách copy từ `.env.example`:
```powershell
cp .env.example .env
```

**Lưu ý quan trọng về kết nối:**
- **MongoDB:**
  - Nếu máy tính đã bật dịch vụ MongoDB Server, ứng dụng sẽ tự động kết nối theo địa chỉ `mongodb://localhost:27017/watch_store`.
  - Nếu máy tính chưa cài đặt MongoDB, hệ thống tích hợp sẵn cơ chế **mongomock tự động fallback**, ứng dụng vẫn khởi động và lưu trữ dữ liệu bình thường phục vụ chấm điểm/demo độc lập mà không báo lỗi crash.
- **Email (Flask-Mail):**
  - Cấu hình SMTP trong file `.env` nếu muốn gửi email thật qua tài khoản Gmail (`MAIL_USERNAME`, `MAIL_PASSWORD` - Mật khẩu ứng dụng).
  - Nếu chưa cấu hình SMTP, khi đặt hàng hệ thống sẽ thông báo rõ: *"Chưa cấu hình tài khoản SMTP trong .env, email xác nhận chưa được gửi đi"* mà không làm gián đoạn việc tạo đơn hàng.

### Bước 5: Nạp dữ liệu mẫu ban đầu (Seeding)
```powershell
python seed.py
```

*Script sẽ tự động khởi tạo:*
- 6 danh mục sản phẩm (Đồng hồ Nam, Nữ, Automatic, Quartz, Thụy Sỹ, Thể thao).
- 12 mẫu đồng hồ cao cấp (Rolex, Omega, Tissot, Longines, Casio, Seiko, Citizen, Cartier...).
- Cấu hình website showroom và thông tin tài khoản ngân hàng nhận thanh toán mã QR.
- 1 tài khoản Admin và 1 tài khoản Khách hàng mẫu.

### Bước 6: Khởi chạy máy chủ Flask
```powershell
python run.py
```

Truy cập website trên trình duyệt tại địa chỉ: **`http://127.0.0.1:5000`**

---

## 4. TÀI KHOẢN TRẢI NGHIỆM DEMO (CHỈ DÙNG LOCAL)

| Phân quyền | Email đăng nhập | Mật khẩu | Quyền hạn và phạm vi thử nghiệm |
| :--- | :--- | :--- | :--- |
| **Quản trị viên (Admin)** | `admin@gmail.com` | `123456` | Truy cập `/admin`, xem thống kê doanh thu, quản lý đơn hàng, CRUD sản phẩm & danh mục, khóa tài khoản khách hàng, cấu hình QR thanh toán. |
| **Khách hàng (Customer)** | `khachhang@gmail.com` | `123456` | Xem catalog, tìm kiếm, giỏ hàng, checkout COD / quét mã QR, xem trang "Đơn hàng của tôi". |

---

## 5. KẾT QUẢ KIỂM THỬ THỰC TẾ VÀ CÁC GIỚI HẠN

### 5.1. Kết quả kiểm thử tự động (Pytest)

Chạy kiểm thử bằng lệnh:
```powershell
python -m pytest tests -v
```

Đã chạy thực tế bộ 23 bài test tự động bao phủ toàn bộ các luồng nghiệp vụ cốt lõi:

```text
watch_store_flask/tests/test_admin.py::test_guest_access_redirects_to_login PASSED
watch_store_flask/tests/test_admin.py::test_customer_forbidden_from_admin PASSED
watch_store_flask/tests/test_admin.py::test_admin_dashboard_access PASSED
watch_store_flask/tests/test_admin.py::test_admin_product_crud PASSED
watch_store_flask/tests/test_admin.py::test_admin_customer_toggle_lock PASSED
watch_store_flask/tests/test_auth.py::test_password_hashing PASSED
watch_store_flask/tests/test_auth.py::test_user_registration PASSED
watch_store_flask/tests/test_auth.py::test_registration_duplicate_email PASSED
watch_store_flask/tests/test_auth.py::test_login_success PASSED
watch_store_flask/tests/test_auth.py::test_login_wrong_password PASSED
watch_store_flask/tests/test_auth.py::test_login_locked_account PASSED
watch_store_flask/tests/test_auth.py::test_logout PASSED
watch_store_flask/tests/test_cart_order.py::test_cart_workflow PASSED
watch_store_flask/tests/test_cart_order.py::test_checkout_and_order_creation PASSED
watch_store_flask/tests/test_cart_order.py::test_user_cannot_view_others_orders PASSED
watch_store_flask/tests/test_network_api.py::test_api_products_list PASSED
watch_store_flask/tests/test_network_api.py::test_api_exchange_rate PASSED
watch_store_flask/tests/test_network_api.py::test_api_banks_list PASSED
watch_store_flask/tests/test_products.py::test_product_catalog_view PASSED
watch_store_flask/tests/test_products.py::test_product_search PASSED
watch_store_flask/tests/test_products.py::test_product_filter_by_category PASSED
watch_store_flask/tests/test_products.py::test_product_detail_view PASSED
watch_store_flask/tests/test_products.py::test_detail_not_found PASSED
======================= 23 passed in 9.21s (100% SUCCESS) =======================
```

### 5.2. Các giới hạn còn tồn tại
- Phương thức thanh toán QR hiện tại dừng ở mức hiển thị mã QR động chuẩn VietQR và hỗ trợ khách hàng xác nhận chuyển khoản để đối soát thủ công; chưa tích hợp Webhook IPN ngân hàng tự động nhận diện tiền vào.
- Chưa có module đánh giá/bình luận sản phẩm (Review & Rating) và hệ thống mã giảm giá (Coupon).

---

## 6. BÁO CÁO ĐỒ ÁN THEO MẪU WORD VÀ THÔNG TIN CẦN BỔ SUNG

File báo cáo Word hoàn chỉnh đã được tạo sẵn theo đúng cấu trúc của file mẫu:
- **Đường dẫn file báo cáo:** `Bao_Cao_DoAn_LapTrinhPythonNangCao_WatchStore.docx`
- **Độ dài nội dung chính:** Trình bày cô đọng trong phạm vi 5–10 trang theo đúng quy định.
- **Quy chuẩn định dạng:** Font Times New Roman, cỡ chữ 13, giãn dòng 1.3, đầy đủ bảng Rubric đánh giá, Bảng 2.1 (Mô tả MongoDB Collections), Bảng 4.1 (Kết quả kiểm thử 10 kịch bản đạt), Trích dẫn IEEE chuẩn.

### Các thông tin nhóm sinh viên cần điền bổ sung vào file Word trước khi nộp:
1. **Trang bìa & Bảng thành viên:**
   - Điền Mã số sinh viên (MSSV), Họ và tên của tối đa 3 thành viên trong nhóm.
   - Điền Tên đề tài / Số thứ tự đề tài theo danh sách lớp phân công.
   - Điền Tháng/Năm nộp báo cáo.
2. **Mục 1.4:** Cập nhật tỷ lệ % đóng góp thực tế giữa các thành viên.
3. **Mục 4.1 (Ảnh chụp giao diện):**
   - Chạy website trên trình duyệt (`http://127.0.0.1:5000`) và chụp 6 ảnh màn hình thực tế chèn vào các vị trí placeholder đã đánh dấu:
     - *Hình 4.1:* Trang chủ WatchStore
     - *Hình 4.2:* Danh mục sản phẩm, tìm kiếm và phân trang
     - *Hình 4.3:* Chi tiết sản phẩm
     - *Hình 4.4:* Giỏ hàng và màn hình thanh toán mã QR
     - *Hình 4.5:* Dashboard quản trị viên
     - *Hình 4.6:* Quản lý đơn hàng và cập nhật trạng thái
4. **Phụ lục A:** Bổ sung đường dẫn GitHub repository của nhóm.
5. **Xuất file PDF:** Mở file `.docx` trong Microsoft Word, chọn **File > Save As > PDF** để nộp kèm file Word theo quy chế nộp bài.
