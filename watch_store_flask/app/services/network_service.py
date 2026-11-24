import json
import logging
import urllib.request
import urllib.error
import requests
from flask import current_app

logger = logging.getLogger(__name__)

# Fallback data if network is unavailable/sandboxed
MOCK_EXCHANGE_RATES = {
    "result": "success",
    "base_code": "USD",
    "rates": {
        "VND": 25450.0,
        "EUR": 0.92,
        "JPY": 155.2,
        "SGD": 1.34,
    },
}

MOCK_BANKS = [
    {"code": "MB", "name": "Ngân hàng TMCP Quân đội", "shortName": "MB Bank"},
    {"code": "VCB", "name": "Ngân hàng TMCP Ngoại thương Việt Nam", "shortName": "Vietcombank"},
    {"code": "TCB", "name": "Ngân hàng TMCP Kỹ thương Việt Nam", "shortName": "Techcombank"},
    {"code": "ACB", "name": "Ngân hàng TMCP Á Châu", "shortName": "ACB"},
    {"code": "BIDV", "name": "Ngân hàng TMCP Đầu tư và Phát triển Việt Nam", "shortName": "BIDV"},
    {"code": "CTG", "name": "Ngân hàng TMCP Công thương Việt Nam", "shortName": "VietinBank"},
    {"code": "VPB", "name": "Ngân hàng TMCP Việt Nam Thịnh Vượng", "shortName": "VPBank"},
]


class NetworkService:
    """Network programming service using urllib and requests for external REST APIs."""

    @classmethod
    def get_usd_to_vnd_rate_urllib(cls):
        """Fetch live exchange rates from Open Exchange API using urllib.request.

        Demonstrates low-level standard library socket/HTTP client with JSON parsing.
        """
        api_url = current_app.config.get("EXCHANGE_RATE_API_URL", "https://open.er-api.com/v6/latest/USD")
        req = urllib.request.Request(
            api_url,
            headers={"User-Agent": "WatchStore-Flask-Client/1.0"},
        )
        try:
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    vnd_rate = data.get("rates", {}).get("VND", 25450.0)
                    return {
                        "source": "live_urllib",
                        "base": data.get("base_code", "USD"),
                        "rate_vnd": float(vnd_rate),
                        "time_last_update_utc": data.get("time_last_update_utc", ""),
                    }
        except (urllib.error.URLError, TimeoutError, Exception) as err:
            logger.warning(f"urllib network request failed ({err}). Using fallback exchange rate data.")

        return {
            "source": "cached_fallback",
            "base": "USD",
            "rate_vnd": MOCK_EXCHANGE_RATES["rates"]["VND"],
            "note": "External API unreachable; using cached financial standard rate.",
        }

    @classmethod
    def get_supported_banks_requests(cls):
        """Fetch list of supported Vietnamese banks using requests library."""
        api_url = current_app.config.get("VIETQR_API_URL", "https://api.vietqr.io/v2/banks")
        try:
            resp = requests.get(api_url, timeout=3, headers={"Accept": "application/json"})
            if resp.status_code == 200:
                json_data = resp.json()
                data_list = json_data.get("data", [])
                if data_list:
                    simplified = [
                        {
                            "code": b.get("code"),
                            "name": b.get("name"),
                            "shortName": b.get("shortName"),
                        }
                        for b in data_list[:15]
                    ]
                    return {"source": "live_requests", "banks": simplified}
        except (requests.RequestException, Exception) as err:
            logger.warning(f"requests network request failed ({err}). Using fallback bank data.")

        return {"source": "cached_fallback", "banks": MOCK_BANKS}

