import os
from typing import List


def get_http_timeout() -> int:
    return int(os.getenv("MFDBA_HTTP_TIMEOUT", "15"))


def get_health_ttl() -> int:
    return int(os.getenv("MFDBA_HEALTH_TTL", "30"))


def get_provider_order() -> List[str]:
    raw = os.getenv("MFDBA_PROVIDER_ORDER", "")
    if not raw:
        return []
    return [p.strip() for p in raw.split(",") if p.strip()]
