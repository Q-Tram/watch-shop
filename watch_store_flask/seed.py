import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.db import get_db
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.order import Order
from app.models.setting import Setting

SAMPLE_CATEGORIES = [
    {"name": "Đồng hồ Nam", "group": "gender", "description": "Bộ sưu tập đồng hồ nam lịch lãm, mạnh mẽ và sang trọng."},
    {"name": "Đồng hồ Nữ", "group": "gender", "description": "Thiết kế thanh lịch, tinh tế và quý phái dành riêng cho phái đẹp."},
    {"name": "Đồng hồ Cơ (Automatic)", "group": "general", "description": "Bộ máy cơ khí tự động lên dây cót tinh xảo đỉnh cao."},
    {"name": "Đồng hồ Quartz", "group": "general", "description": "Bộ máy pin thạch anh hoạt động bền bỉ, độ chính xác tuyệt đối."},
    {"name": "Đồng hồ Thụy Sỹ", "group": "brand", "description": "Tiêu chuẩn Swiss Made đỉnh cao truyền thống lâu đời."},
    {"name": "Đồng hồ Thể thao", "group": "general", "description": "Khả năng chống va đập, chống nước 100m-300m chuyên dụng."},
]

SAMPLE_PRODUCTS = [
    {
        "name": "Rolex Submariner Date 41mm",
        "price": 385000000,
        "brand": "Rolex",
        "category": "Đồng hồ Nam",
        "stock": 5,
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80",
        "description": "Rolex Submariner Date bằng thép Oystersteel, vành Cerachrom bằng gốm đen, mặt số đen và các mốc giờ phát quang Chromalight lớn. Chống nước 300m.",
        "status": "Hiện",
    },
    {
        "name": "Omega Speedmaster Moonwatch Professional",
        "price": 195000000,
        "brand": "Omega",
        "category": "Đồng hồ Cơ (Automatic)",
        "stock": 8,
        "image": "https://images.unsplash.com/photo-1547996160-71dfabbce5ed?auto=format&fit=crop&w=800&q=80",
        "description": "Chiếc đồng hồ chronograph huyền thoại đã đồng hành cùng các phi hành gia trong 6 lần đổ bộ lên mặt trăng. Bộ máy Co-Axial Master Chronometer Calibre 3861.",
        "status": "Hiện",
    },
    {
        "name": "Tissot Le Locle Powermatic 80",
        "price": 18500000,
        "brand": "Tissot",
        "category": "Đồng hồ Nam",
        "stock": 15,
        "image": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?auto=format&fit=crop&w=800&q=80",
        "description": "Biểu tượng thanh lịch cổ điển của Tissot. Mặt số hoa văn Clous de Paris, số La Mã cổ điển, khả năng trữ cót ấn tượng lên đến 80 giờ.",
        "status": "Hiện",
    },
    {
        "name": "Longines Master Collection Diamond",
        "price": 68000000,
        "brand": "Longines",
        "category": "Đồng hồ Nữ",
        "stock": 7,
        "image": "https://images.unsplash.com/photo-1542496658-e33a6d0d50f6?auto=format&fit=crop&w=800&q=80",
        "description": "Mặt số xà cừ tự nhiên đính 12 viên kim cương lấp lánh (Wesselton VVS), kim nung xanh đặc trưng, kính Sapphire nguyên khối chống trầy.",
        "status": "Hiện",
    },
    {
        "name": "Seiko Presage Cocktail Time 'Blue Moon'",
        "price": 12800000,
        "brand": "Seiko",
        "category": "Đồng hồ Cơ (Automatic)",
        "stock": 20,
        "image": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=800&q=80",
        "description": "Lấy cảm hứng từ ly cocktail Blue Moon tại quán bar Tokyo. Mặt số xanh Guilloche ánh sáng tỏa tia tuyệt mỹ, bộ máy in-house 4R35 bền bỉ.",
        "status": "Hiện",
    },
    {
        "name": "Casio G-Shock GA-2100 'CasiOak'",
        "price": 3500000,
        "brand": "Casio",
        "category": "Đồng hồ Thể thao",
        "stock": 30,
        "image": "https://images.unsplash.com/photo-1533139502658-0198f920d8e8?auto=format&fit=crop&w=800&q=80",
        "description": "Cấu trúc bảo vệ lõi carbon siêu nhẹ và chống sốc huyền thoại. Thiết kế vành bát giác mang tính biểu tượng, chống nước 200m.",
        "status": "Hiện",
    },
    {
        "name": "Citizen Eco-Drive Promaster Diver",
        "price": 8900000,
        "brand": "Citizen",
        "category": "Đồng hồ Thể thao",
        "stock": 12,
        "image": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?auto=format&fit=crop&w=800&q=80",
        "description": "Công nghệ Eco-Drive hấp thu bất kỳ nguồn ánh sáng nào để nạp năng lượng, không cần thay pin. Đạt chuẩn đồng hồ lặn ISO 6425, chịu nước 200m.",
        "status": "Hiện",
    },
    {
        "name": "Cartier Tank Must de Cartier",
        "price": 88000000,
        "brand": "Cartier",
        "category": "Đồng hồ Nữ",
        "stock": 4,
        "image": "https://images.unsplash.com/photo-1539185441755-769473a23570?auto=format&fit=crop&w=800&q=80",
        "description": "Hình mẫu kinh điển của sự sang trọng quý phái phong cách Pháp. Vỏ hình chữ nhật tinh giản, kim nung xanh hình thanh kiếm, núm vặn đính đá spinel.",
        "status": "Hiện",
    },
    {
        "name": "Tag Heuer Carrera Chronograph 44mm",
        "price": 145000000,
        "brand": "Tag Heuer",
        "category": "Đồng hồ Nam",
        "stock": 6,
        "image": "https://images.unsplash.com/photo-1526045478516-99145907023c?auto=format&fit=crop&w=800&q=80",
        "description": "Đồng hồ thể thao đua xe đỉnh cao. Bộ máy Calibre HEUER02 tự động trữ cót 80 giờ, vành bezel gốm ceramic thang đo Tachymetre đo tốc độ.",
        "status": "Hiện",
    },
    {
        "name": "Tissot PRX Powermatic 80 Ice Blue",
        "price": 19800000,
        "brand": "Tissot",
        "category": "Đồng hồ Nam",
        "stock": 14,
        "image": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?auto=format&fit=crop&w=800&q=80",
        "description": "Cơn sốt đồng hồ thể thao dây tích hợp phong cách thập niên 70. Mặt số hoa văn dập nổi màu xanh băng tuyết (Ice Blue) mê hoặc.",
        "status": "Hiện",
    },
    {
        "name": "Orient Star Contemporary Open Heart",
        "price": 16500000,
        "brand": "Orient",
        "category": "Đồng hồ Cơ (Automatic)",
        "stock": 9,
        "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=800&q=80",
        "description": "Thiết kế hở tim lộ cơ góc 9 giờ khoe chuyển động nhịp nhàng của bánh đà cân bằng. Thang đo kim xăng hiển thị năng lượng cót 50 giờ.",
        "status": "Hiện",
    },
    {
        "name": "Casio Edifice Bluetooth Solar",
        "price": 5400000,
        "brand": "Casio",
        "category": "Đồng hồ Quartz",
        "stock": 18,
        "image": "https://images.unsplash.com/photo-1594576722512-582bcd46fba3?auto=format&fit=crop&w=800&q=80",
        "description": "Kết nối điện thoại thông minh qua Bluetooth tự động cập nhật giờ quốc tế chính xác. Nạp năng lượng mặt trời Tough Solar tiên tiến.",
        "status": "Hiện",
    },
]


def seed_database():
    """Populate database with clean demonstration data."""
    app = create_app()
    with app.app_context():
        db = get_db()
        print("🌱 Bắt đầu khởi tạo dữ liệu mẫu (Seeding)...")

        # 1. Seed Accounts
        admin = User.find_by_email("admin@gmail.com")
        if not admin:
            admin = User.create(
                fullName="Quản Trị Viên",
                email="admin@gmail.com",
                password="123456",
                phone="0909999999",
                address="Tòa nhà WatchStore Center, Quận 1, TP.HCM",
                role="admin",
            )
            print("  ✅ Tạo tài khoản Admin: admin@gmail.com / 123456")
        else:
            print("  ℹ️ Tài khoản Admin đã tồn tại.")

        customer = User.find_by_email("khachhang@gmail.com")
        if not customer:
            customer = User.create(
                fullName="Nguyễn Văn An",
                email="khachhang@gmail.com",
                password="123456",
                phone="0901234567",
                address="233 Nguyễn Văn Cừ, Phường 4, Quận 5, TP.HCM",
                role="customer",
            )
            print("  ✅ Tạo tài khoản Khách hàng: khachhang@gmail.com / 123456")
        else:
            print("  ℹ️ Tài khoản Khách hàng đã tồn tại.")

        # 2. Seed Categories
        for cat in SAMPLE_CATEGORIES:
            existing = Category.find_by_slug(cat["name"])
            if not existing:
                Category.create(
                    name=cat["name"],
                    description=cat["description"],
                    group=cat["group"],
                )
        print(f"  ✅ Đã khởi tạo {len(SAMPLE_CATEGORIES)} danh mục sản phẩm.")

        # 3. Seed Products
        if db.products.count_documents({}) == 0:
            for p in SAMPLE_PRODUCTS:
                Product.create(
                    name=p["name"],
                    price=p["price"],
                    brand=p["brand"],
                    category=p["category"],
                    stock=p["stock"],
                    image=p["image"],
                    description=p["description"],
                    status=p["status"],
                )
            print(f"  ✅ Đã khởi tạo {len(SAMPLE_PRODUCTS)} mẫu đồng hồ cao cấp.")
        else:
            print(f"  ℹ️ Sản phẩm đã tồn tại ({db.products.count_documents({})} sản phẩm).")

        # 4. Seed Settings
        Setting.get_website_settings()
        Setting.get_payment_settings()
        print("  ✅ Đã khởi tạo cấu hình website và thanh toán chuyển khoản QR.")

        # 5. Seed a demo order for the sample customer if no orders
        if db.orders.count_documents({}) == 0 and customer:
            first_prod = Product.get_featured(1)
            if first_prod:
                fp = first_prod[0]
                Order.create(
                    user_id=customer.id,
                    items=[{
                        "product": fp.id,
                        "name": fp.name,
                        "price": fp.price,
                        "image": fp.image,
                        "quantity": 1,
                    }],
                    shipping_info={
                        "fullName": customer.fullName,
                        "phone": customer.phone,
                        "address": customer.address,
                        "note": "Giao hàng giờ hành chính",
                    },
                    payment_method="QR",
                    payment_status="paid",
                    total_amount=fp.price,
                )
                print("  ✅ Tạo đơn hàng mẫu thành công.")

        print("🎉 Hoàn tất nạp dữ liệu mẫu vào MongoDB thành công!")


if __name__ == "__main__":
    seed_database()

