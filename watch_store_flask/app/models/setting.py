from datetime import datetime, timezone
from app.db import get_db

DEFAULT_WEBSITE_SETTINGS = {
    "key": "website",
    "siteName": "WatchStore",
    "footerDescription": "Cửa hàng đồng hồ chính hãng với nhiều mẫu mã hiện đại, phù hợp cho mọi phong cách.",
    "logoUrl": "",
    "contactEmail": "support@watchstore.com",
    "contactPhone": "+84 123 456 789",
    "contactAddress": "233 Nguyễn Văn Cừ, Quận 5, TP. Hồ Chí Minh",
    "workingHours": "Thứ 2 – Thứ 7 | 08:00 – 21:00",
    "contactSlogan": "YOUR TIME, YOUR STYLE.",
    "facebookUrl": "https://facebook.com",
    "instagramUrl": "https://instagram.com",
    "tiktokUrl": "https://tiktok.com",
}

DEFAULT_PAYMENT_SETTINGS = {
    "key": "payment",
    "bankName": "MB BANK",
    "accountNumber": "123456789",
    "accountName": "WATCH STORE",
    "transferContent": "Thanh toan don hang WatchStore",
    "isQrEnabled": True,
    "qrImage": "",
}


class Setting:
    """Website & Payment settings repository."""

    @staticmethod
    def get_collection():
        return get_db().settings

    @classmethod
    def get_website_settings(cls):
        doc = cls.get_collection().find_one({"key": "website"})
        if not doc:
            data = DEFAULT_WEBSITE_SETTINGS.copy()
            data["createdAt"] = datetime.now(timezone.utc)
            cls.get_collection().insert_one(data)
            return data
        return doc

    @classmethod
    def update_website_settings(cls, data):
        now = datetime.now(timezone.utc)
        clean = {
            "siteName": data.get("siteName", "").strip() or "WatchStore",
            "footerDescription": data.get("footerDescription", "").strip(),
            "logoUrl": data.get("logoUrl", "").strip(),
            "contactEmail": data.get("contactEmail", "").strip(),
            "contactPhone": data.get("contactPhone", "").strip(),
            "contactAddress": data.get("contactAddress", "").strip(),
            "workingHours": data.get("workingHours", "").strip(),
            "contactSlogan": data.get("contactSlogan", "").strip(),
            "facebookUrl": data.get("facebookUrl", "").strip(),
            "instagramUrl": data.get("instagramUrl", "").strip(),
            "tiktokUrl": data.get("tiktokUrl", "").strip(),
            "updatedAt": now,
        }
        cls.get_collection().update_one(
            {"key": "website"},
            {"$set": clean},
            upsert=True,
        )
        return cls.get_website_settings()

    @classmethod
    def get_payment_settings(cls):
        doc = cls.get_collection().find_one({"key": "payment"})
        if not doc:
            data = DEFAULT_PAYMENT_SETTINGS.copy()
            data["createdAt"] = datetime.now(timezone.utc)
            cls.get_collection().insert_one(data)
            return data
        return doc

    @classmethod
    def update_payment_settings(cls, data):
        now = datetime.now(timezone.utc)
        clean = {
            "bankName": data.get("bankName", "").strip() or "MB BANK",
            "accountNumber": data.get("accountNumber", "").strip() or "123456789",
            "accountName": data.get("accountName", "").strip() or "WATCH STORE",
            "transferContent": data.get("transferContent", "").strip() or "Thanh toan don hang WatchStore",
            "isQrEnabled": bool(data.get("isQrEnabled", True)),
            "qrImage": data.get("qrImage", "").strip(),
            "updatedAt": now,
        }
        cls.get_collection().update_one(
            {"key": "payment"},
            {"$set": clean},
            upsert=True,
        )
        return cls.get_payment_settings()

