import os
from app import create_app

env_name = os.getenv("FLASK_ENV", "development")
app = create_app(env_name)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")
    print(f"🚀 WatchStore Flask Server đang chạy tại http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)

