from datetime import datetime, timezone
from bson.objectid import ObjectId
from app.db import get_db


ORDER_STATUSES = ["pending", "confirmed", "shipping", "delivered", "cancelled"]
PAYMENT_METHODS = ["COD", "QR"]
PAYMENT_STATUSES = ["unpaid", "paid"]

ORDER_STATUS_LABELS = {
    "pending": "Chờ xác nhận",
    "confirmed": "Đã xác nhận",
    "shipping": "Đang giao",
    "delivered": "Đã giao",
    "cancelled": "Đã hủy",
}

ORDER_STATUS_BADGES = {
    "pending": "warning",
    "confirmed": "info",
    "shipping": "primary",
    "delivered": "success",
    "cancelled": "danger",
}


class Order:
    """Order model and repository for MongoDB."""

    def __init__(self, doc):
        self._doc = doc or {}
        self.id = str(self._doc.get("_id", ""))
        self.user_id = str(self._doc.get("user", ""))
        self.items = self._doc.get("items", [])
        self.shippingInfo = self._doc.get("shippingInfo", {})
        self.paymentMethod = self._doc.get("paymentMethod", "COD")
        self.paymentStatus = self._doc.get("paymentStatus", "unpaid")
        self.orderStatus = self._doc.get("orderStatus", "pending")
        self.totalAmount = float(self._doc.get("totalAmount", 0.0))
        self.createdAt = self._doc.get("createdAt")
        self.updatedAt = self._doc.get("updatedAt")
        self.user_info = self._doc.get("user_info", None)

    @property
    def status_label(self):
        return ORDER_STATUS_LABELS.get(self.orderStatus, self.orderStatus)

    @property
    def status_badge(self):
        return ORDER_STATUS_BADGES.get(self.orderStatus, "secondary")

    @property
    def is_paid(self):
        return self.paymentStatus == "paid"

    def to_dict(self):
        return {
            "id": self.id,
            "_id": self.id,
            "user": self.user_id,
            "items": self.items,
            "shippingInfo": self.shippingInfo,
            "paymentMethod": self.paymentMethod,
            "paymentStatus": self.paymentStatus,
            "orderStatus": self.orderStatus,
            "totalAmount": self.totalAmount,
            "statusLabel": self.status_label,
            "createdAt": self.createdAt.isoformat() if isinstance(self.createdAt, datetime) else str(self.createdAt),
            "updatedAt": self.updatedAt.isoformat() if isinstance(self.updatedAt, datetime) else str(self.updatedAt),
        }

    @staticmethod
    def get_collection():
        return get_db().orders

    @classmethod
    def create(cls, user_id, items, shipping_info, payment_method="COD", payment_status="unpaid", total_amount=0.0):
        now = datetime.now(timezone.utc)
        clean_items = []
        for it in items:
            clean_items.append({
                "product": str(it.get("product", "")),
                "name": it.get("name", ""),
                "price": float(it.get("price", 0.0)),
                "image": it.get("image", ""),
                "quantity": int(it.get("quantity", 1)),
            })

        doc = {
            "user": ObjectId(user_id) if ObjectId.is_valid(user_id) else user_id,
            "items": clean_items,
            "shippingInfo": {
                "fullName": shipping_info.get("fullName", "").strip(),
                "phone": shipping_info.get("phone", "").strip(),
                "address": shipping_info.get("address", "").strip(),
                "note": shipping_info.get("note", "").strip(),
            },
            "paymentMethod": payment_method if payment_method in PAYMENT_METHODS else "COD",
            "paymentStatus": payment_status if payment_status in PAYMENT_STATUSES else "unpaid",
            "orderStatus": "pending",
            "totalAmount": float(total_amount),
            "createdAt": now,
            "updatedAt": now,
        }
        res = cls.get_collection().insert_one(doc)
        doc["_id"] = res.inserted_id
        return cls(doc)

    @classmethod
    def find_by_id(cls, order_id):
        try:
            doc = cls.get_collection().find_one({"_id": ObjectId(order_id)})
            if not doc:
                return None
            order = cls(doc)
            # Attach user info if user is ObjectId
            user_doc = get_db().users.find_one({"_id": doc.get("user")})
            if user_doc:
                order.user_info = {
                    "fullName": user_doc.get("fullName", ""),
                    "email": user_doc.get("email", ""),
                }
            return order
        except Exception:
            return None

    @classmethod
    def find_by_user(cls, user_id, page=1, per_page=10):
        try:
            uid = ObjectId(user_id) if ObjectId.is_valid(user_id) else user_id
            query = {"user": uid}
            col = cls.get_collection()
            total = col.count_documents(query)
            cursor = (
                col.find(query)
                .sort("createdAt", -1)
                .skip((page - 1) * per_page)
                .limit(per_page)
            )
            orders = [cls(doc) for doc in cursor]
            total_pages = max(1, (total + per_page - 1) // per_page)
            return orders, total, total_pages
        except Exception:
            return [], 0, 1

    @classmethod
    def find_all_paginated(cls, status=None, search=None, page=1, per_page=10):
        query = {}
        if status and status != "all":
            query["orderStatus"] = status

        if search:
            regex = {"$regex": search.strip(), "$options": "i"}
            query["$or"] = [
                {"shippingInfo.fullName": regex},
                {"shippingInfo.phone": regex},
                {"shippingInfo.address": regex},
            ]

        col = cls.get_collection()
        total = col.count_documents(query)
        cursor = (
            col.find(query)
            .sort("createdAt", -1)
            .skip((page - 1) * per_page)
            .limit(per_page)
        )
        orders = []
        for doc in cursor:
            order = cls(doc)
            user_doc = get_db().users.find_one({"_id": doc.get("user")})
            if user_doc:
                order.user_info = {
                    "fullName": user_doc.get("fullName", ""),
                    "email": user_doc.get("email", ""),
                }
            orders.append(order)

        total_pages = max(1, (total + per_page - 1) // per_page)
        return orders, total, total_pages

    @classmethod
    def update_status(cls, order_id, new_status):
        if new_status not in ORDER_STATUSES:
            return False
        now = datetime.now(timezone.utc)
        res = cls.get_collection().update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"orderStatus": new_status, "updatedAt": now}},
        )
        return res.modified_count > 0

    @classmethod
    def update_payment_status(cls, order_id, new_payment_status):
        if new_payment_status not in PAYMENT_STATUSES:
            return False
        now = datetime.now(timezone.utc)
        res = cls.get_collection().update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"paymentStatus": new_payment_status, "updatedAt": now}},
        )
        return res.modified_count > 0

    @classmethod
    def get_dashboard_stats(cls):
        col = cls.get_collection()
        total_orders = col.count_documents({})
        total_customers = get_db().users.count_documents({"role": "customer"})
        total_products = get_db().products.count_documents({})

        # Total revenue
        revenue = 0.0
        for doc in col.find({"orderStatus": {"$ne": "cancelled"}}):
            revenue += float(doc.get("totalAmount", 0.0))

        # Status counts
        status_counts = {s: col.count_documents({"orderStatus": s}) for s in ORDER_STATUSES}

        # Recent 5 orders
        recent_orders_raw = list(col.find().sort("createdAt", -1).limit(5))
        recent_orders = []
        for doc in recent_orders_raw:
            order = cls(doc)
            user_doc = get_db().users.find_one({"_id": doc.get("user")})
            if user_doc:
                order.user_info = {
                    "fullName": user_doc.get("fullName", ""),
                    "email": user_doc.get("email", ""),
                }
            recent_orders.append(order)

        return {
            "total_revenue": revenue,
            "total_orders": total_orders,
            "total_customers": total_customers,
            "total_products": total_products,
            "status_counts": status_counts,
            "recent_orders": recent_orders,
        }

