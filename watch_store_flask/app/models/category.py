import re
import unicodedata
from datetime import datetime, timezone
from bson.objectid import ObjectId
from app.db import get_db


def to_slug(text):
    """Generate a clean URL-friendly slug from text."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text)


class Category:
    """Category model and repository for MongoDB."""

    def __init__(self, doc):
        self._doc = doc or {}
        self.id = str(self._doc.get("_id", ""))
        self.name = self._doc.get("name", "")
        self.slug = self._doc.get("slug", "")
        self.group = self._doc.get("group", "general")
        self.value = self._doc.get("value", "")
        self.description = self._doc.get("description", "")
        self.createdAt = self._doc.get("createdAt")
        self.updatedAt = self._doc.get("updatedAt")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "group": self.group,
            "value": self.value,
            "description": self.description,
            "createdAt": self.createdAt.isoformat() if isinstance(self.createdAt, datetime) else str(self.createdAt),
        }

    @staticmethod
    def get_collection():
        return get_db().categories

    @classmethod
    def find_all(cls, group=None):
        query = {}
        if group:
            query["group"] = group
        cursor = cls.get_collection().find(query).sort("name", 1)
        return [cls(doc) for doc in cursor]

    @classmethod
    def find_by_id(cls, category_id):
        try:
            doc = cls.get_collection().find_one({"_id": ObjectId(category_id)})
            return cls(doc) if doc else None
        except Exception:
            return None

    @classmethod
    def find_by_slug(cls, slug):
        if not slug:
            return None
        doc = cls.get_collection().find_one({"slug": slug.strip().lower()})
        return cls(doc) if doc else None

    @classmethod
    def create(cls, name, description="", group="general", value=""):
        slug = to_slug(name)
        now = datetime.now(timezone.utc)
        doc = {
            "name": name.strip(),
            "slug": slug,
            "group": group.strip() if group else "general",
            "value": value.strip() if value else name.strip(),
            "description": description.strip() if description else "",
            "createdAt": now,
            "updatedAt": now,
        }
        res = cls.get_collection().insert_one(doc)
        doc["_id"] = res.inserted_id
        return cls(doc)

    @classmethod
    def update(cls, category_id, name, description="", group="general", value=""):
        slug = to_slug(name)
        now = datetime.now(timezone.utc)
        cls.get_collection().update_one(
            {"_id": ObjectId(category_id)},
            {
                "$set": {
                    "name": name.strip(),
                    "slug": slug,
                    "group": group.strip() if group else "general",
                    "value": value.strip() if value else name.strip(),
                    "description": description.strip() if description else "",
                    "updatedAt": now,
                }
            },
        )
        return cls.find_by_id(category_id)

    @classmethod
    def delete(cls, category_id):
        try:
            res = cls.get_collection().delete_one({"_id": ObjectId(category_id)})
            return res.deleted_count > 0
        except Exception:
            return False

