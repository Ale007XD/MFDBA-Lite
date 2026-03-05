# mfdballm/config.py

import os
from typing import List
from pathlib import Path

# ============================================================
# HTTP / Networking
# ============================================================

DEFAULT_HTTP_TIMEOUT = 15


def get_http_timeout() -> int:
    return int(os.getenv("MFDBA_HTTP_TIMEOUT", str(DEFAULT_HTTP_TIMEOUT)))


# ============================================================
# Health Cache
# ============================================================

DEFAULT_HEALTH_TTL = 30


def get_health_ttl() -> int:
    return int(os.getenv("MFDBA_HEALTH_TTL", str(DEFAULT_HEALTH_TTL)))


# ============================================================
# Circuit Breaker Configuration (v0.9.0)
# ============================================================

DEFAULT_FAILURE_THRESHOLD = 3
DEFAULT_RECOVERY_TIMEOUT = 30
DEFAULT_HALF_OPEN_MAX_REQUESTS = 1

DEFAULT_MAX_RETRIES = 3
DEFAULT_BASE_BACKOFF = 1.0


def get_failure_threshold() -> int:
    return int(os.getenv("MFDBA_FAILURE_THRESHOLD", str(DEFAULT_FAILURE_THRESHOLD)))


def get_recovery_timeout() -> int:
    return int(os.getenv("MFDBA_RECOVERY_TIMEOUT", str(DEFAULT_RECOVERY_TIMEOUT)))


def get_half_open_max_requests() -> int:
    return int(
        os.getenv(
            "MFDBA_HALF_OPEN_MAX_REQUESTS",
            str(DEFAULT_HALF_OPEN_MAX_REQUESTS),
        )
    )


def get_max_retries() -> int:
    return int(os.getenv("MFDBA_MAX_RETRIES", str(DEFAULT_MAX_RETRIES)))


def get_base_backoff() -> float:
    return float(os.getenv("MFDBA_BASE_BACKOFF", str(DEFAULT_BASE_BACKOFF)))


# ============================================================
# Provider Order
# ============================================================

DEFAULT_PROVIDER_ORDER = ["groq", "openrouter", "gemini"]


def get_provider_order() -> List[str]:
    raw = os.getenv("MFDBA_PROVIDER_ORDER", "").strip()

    if not raw:
        return DEFAULT_PROVIDER_ORDER.copy()

    order = [
        p.strip().lower()
        for p in raw.split(",")
        if p.strip()
    ]

    if not order:
        return DEFAULT_PROVIDER_ORDER.copy()

    return order


# ============================================================
# Gemini Configuration
# ============================================================

DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"


def get_gemini_model() -> str:
    return os.getenv("MFDBA_GEMINI_MODEL", DEFAULT_GEMINI_MODEL)


# ============================================================
# Session Root
# ============================================================

def get_sessions_root() -> Path:
    return Path.home() / ".mfdballm" / "sessions"
