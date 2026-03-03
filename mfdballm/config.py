# mfdballm/config.py

import os
from typing import List
from pathlib import Path

# ============================================================
# Global Configuration
# ============================================================

# -----------------------------
# HTTP / Networking
# -----------------------------

DEFAULT_HTTP_TIMEOUT = 15


def get_http_timeout() -> int:
    return int(os.getenv("MFDBA_HTTP_TIMEOUT", str(DEFAULT_HTTP_TIMEOUT)))


# -----------------------------
# Health Cache
# -----------------------------

DEFAULT_HEALTH_TTL = 30


def get_health_ttl() -> int:
    return int(os.getenv("MFDBA_HEALTH_TTL", str(DEFAULT_HEALTH_TTL)))


# -----------------------------
# Router Behavior
# -----------------------------

DEFAULT_MAX_RETRIES = 3
DEFAULT_BASE_BACKOFF = 1.0


def get_max_retries() -> int:
    return int(os.getenv("MFDBA_MAX_RETRIES", str(DEFAULT_MAX_RETRIES)))


def get_base_backoff() -> float:
    return float(os.getenv("MFDBA_BASE_BACKOFF", str(DEFAULT_BASE_BACKOFF)))


# -----------------------------
# Provider Order
# -----------------------------

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


# -----------------------------
# Gemini Configuration
# -----------------------------

DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"


def get_gemini_model() -> str:
    """
    Returns Gemini model name without 'models/' prefix.
    Must match Google ListModels output.
    """
    return os.getenv("MFDBA_GEMINI_MODEL", DEFAULT_GEMINI_MODEL)


# -----------------------------
# Session Root
# -----------------------------

def get_sessions_root() -> Path:
    return Path.home() / ".mfdballm" / "sessions"
