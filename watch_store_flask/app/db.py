import logging
import pymongo
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

logger = logging.getLogger(__name__)

_mongo_client = None
_db = None


def init_db(app):
    """Initialize MongoDB connection.

    Supports real MongoDB (PyMongo) and fallback to mongomock when configured or
    when local MongoDB is unavailable during development/testing.
    """
    global _mongo_client, _db

    uri = app.config.get("MONGO_URI", "mongodb://localhost:27017/watch_store")
    use_mock = app.config.get("USE_MONGOMOCK", False)

    if use_mock:
        logger.info("Initializing in-memory mongomock database...")
        import mongomock
        _mongo_client = mongomock.MongoClient()
        _db = _mongo_client["watch_store"]
    else:
        try:
            logger.info(f"Connecting to MongoDB at {uri}...")
            _mongo_client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=2000)
            # Trigger a command to verify connection
            _mongo_client.admin.command("ping")
            db_name = uri.split("/")[-1].split("?")[0] or "watch_store"
            _db = _mongo_client[db_name]
            logger.info(f"Successfully connected to MongoDB database '{db_name}'.")
        except (ConnectionFailure, ServerSelectionTimeoutError) as err:
            if app.config.get("DEBUG", False) or app.config.get("TESTING", False):
                logger.warning(
                    f"Could not connect to MongoDB ({err}). "
                    f"Falling back to in-memory mongomock for development/testing."
                )
                import mongomock
                _mongo_client = mongomock.MongoClient()
                _db = _mongo_client["watch_store"]
            else:
                raise err

    # Ensure indexes
    setup_indexes(_db)
    return _db


def get_db():
    """Retrieve the current database instance."""
    global _db
    if _db is None:
        raise RuntimeError("Database not initialized. Call init_db(app) first.")
    return _db


def setup_indexes(db):
    """Create essential MongoDB indexes."""
    try:
        # User collection indexes
        db.users.create_index("email", unique=True)
        db.users.create_index("role")

        # Category collection indexes
        db.categories.create_index("slug", unique=True)
        db.categories.create_index("group")

        # Product collection indexes
        db.products.create_index([("name", pymongo.TEXT), ("description", pymongo.TEXT), ("brand", pymongo.TEXT)])
        db.products.create_index("category")
        db.products.create_index("brand")
        db.products.create_index("status")
        db.products.create_index("price")

        # Order collection indexes
        db.orders.create_index("user")
        db.orders.create_index("orderStatus")
        db.orders.create_index("createdAt")

        # Setting collection indexes
        db.settings.create_index("key", unique=True)
        logger.info("MongoDB indexes verified/created successfully.")
    except Exception as e:
        logger.warning(f"Note on index creation: {e}")

