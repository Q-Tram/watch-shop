from datetime import datetime, timezone
from bson.objectid import ObjectId
from app.db import get_db


class Product:
    """Product model and repository for MongoDB."""

    def __init__(self, doc):
        self._doc = doc or {}
        self.id = str(self._doc.get("_id", ""))
        self.name = self._doc.get("name", "")
        self.price = float(self._doc.get("price", 0.0))
        self.image = self._doc.get("image", "")
        self.description = self._doc.get("description", "")
        self.brand = self._doc.get("brand", "")
        self.category = self._doc.get("category", "")
        self.stock = int(self._doc.get("stock", 0))
        self.status = self._doc.get("status", "Hiện")
        self.createdAt = self._doc.get("createdAt")
        self.updatedAt = self._doc.get("updatedAt")

    @property
    def is_visible(self):
        return self.status != "Ẩn"

    @property
    def in_stock(self):
        return self.stock > 0

    def to_dict(self):
        return {
            "id": self.id,
            "_id": self.id,
            "name": self.name,
            "price": self.price,
            "image": self.image,
            "description": self.description,
            "brand": self.brand,
            "category": self.category,
            "stock": self.stock,
            "status": self.status,
            "createdAt": self.createdAt.isoformat() if isinstance(self.createdAt, datetime) else str(self.createdAt),
        }

    @staticmethod
    def get_collection():
        return get_db().products

    @classmethod
    def find_by_id(cls, product_id):
        try:
            doc = cls.get_collection().find_one({"_id": ObjectId(product_id)})
            return cls(doc) if doc else None
        except Exception:
            return None

    @classmethod
    def find_filtered_and_paginated(
        cls,
        keyword=None,
        category=None,
        brand=None,
        status="Hiện",
        min_price=None,
        max_price=None,
        sort_by="newest",
        page=1,
        per_page=8,
    ):
        query = {}
        if status:
            query["status"] = status

        if keyword:
            regex = {"$regex": keyword.strip(), "$options": "i"}
            query["$or"] = [
                {"name": regex},
                {"brand": regex},
                {"description": regex},
            ]

        if category and category.lower() != "all":
            query["category"] = {"$regex": f"^{category.strip()}$", "$options": "i"}

        if brand and brand.lower() != "all":
            query["brand"] = {"$regex": f"^{brand.strip()}$", "$options": "i"}

        if min_price is not None or max_price is not None:
            price_query = {}
            if min_price is not None:
                price_query["$gte"] = float(min_price)
            if max_price is not None:
                price_query["$lte"] = float(max_price)
            query["price"] = price_query

        # Sorting
        sort_rule = [("createdAt", -1)]
        if sort_by == "price_asc":
            sort_rule = [("price", 1)]
        elif sort_by == "price_desc":
            sort_rule = [("price", -1)]
        elif sort_by == "name_asc":
            sort_rule = [("name", 1)]

        col = cls.get_collection()
        total = col.count_documents(query)
        cursor = (
            col.find(query)
            .sort(sort_rule)
            .skip((page - 1) * per_page)
            .limit(per_page)
        )
        products = [cls(doc) for doc in cursor]
        total_pages = max(1, (total + per_page - 1) // per_page)

        return products, total, total_pages

    @classmethod
    def get_featured(cls, limit=4):
        cursor = (
            cls.get_collection()
            .find({"status": "Hiện"})
            .sort("createdAt", -1)
            .limit(limit)
        )
        return [cls(doc) for doc in cursor]

    @classmethod
    def create(cls, name, price, brand="", category="", stock=0, image="", description="", status="Hiện"):
        now = datetime.now(timezone.utc)
        doc = {
            "name": name.strip(),
            "price": float(price),
            "brand": brand.strip() if brand else "",
            "category": category.strip() if category else "",
            "stock": int(stock),
            "image": image.strip() if image else "",
            "description": description.strip() if description else "",
            "status": status if status in ("Hiện", "Ẩn") else "Hiện",
            "createdAt": now,
            "updatedAt": now,
        }
        res = cls.get_collection().insert_one(doc)
        doc["_id"] = res.inserted_id
        return cls(doc)

    @classmethod
    def update(cls, product_id, name, price, brand="", category="", stock=0, image="", description="", status="Hiện"):
        now = datetime.now(timezone.utc)
        cls.get_collection().update_one(
            {"_id": ObjectId(product_id)},
            {
                "$set": {
                    "name": name.strip(),
                    "price": float(price),
                    "brand": brand.strip() if brand else "",
                    "category": category.strip() if category else "",
                    "stock": int(stock),
                    "image": image.strip() if image else "",
                    "description": description.strip() if description else "",
                    "status": status if status in ("Hiện", "Ẩn") else "Hiện",
                    "updatedAt": now,
                }
            },
        )
        return cls.find_by_id(product_id)

    @classmethod
    def delete(cls, product_id):
        try:
            res = cls.get_collection().delete_one({"_id": ObjectId(product_id)})
            return res.deleted_count > 0
        except Exception:
            return False

    @classmethod
    def decrement_stock(cls, product_id, quantity):
        """Atomically decrement stock if enough inventory is available."""
        res = cls.get_collection().update_one(
            {"_id": ObjectId(product_id), "stock": {"$gte": quantity}},
            {"$inc": {"stock": -quantity}, "$set": {"updatedAt": datetime.now(timezone.utc)}},
        )
        return res.modified_count > 0

    @classmethod
    def get_distinct_categories(cls):
        return sorted([c for c in cls.get_collection().distinct("category") if c])

    @classmethod
    def get_distinct_brands(cls):
        return sorted([b for b in cls.get_collection().distinct("brand") if b])

