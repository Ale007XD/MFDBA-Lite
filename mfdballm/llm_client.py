import os
import time
import logging
import requests
from typing import List, Dict, Optional

from mfdballm.rate_limiter import RateLimiter

logger = logging.getLogger("mfdballm.llm_client")


class LLMClient:

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    DEFAULT_MODELS = [
        "google/gemma-3-12b-it:free",
        "google/gemma-3-4b-it:free",
        "liquid/lfm-2.5-1.2b-instruct:free",
    ]

    def __init__(
        self,
        api_key: Optional[str] = None,
        models: Optional[List[str]] = None,
    ):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY not set")

        self.models = models or self.DEFAULT_MODELS

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://localhost",
            "X-Title": "MFDBA-LLMClient",
        }

        self.limiter = RateLimiter(
            max_requests=8,
            window_seconds=60,
            min_delay=6,
        )

    def chat(
        self,
        messages: List[Dict],
        temperature: float = 0.2,
        max_tokens: int = 2000,
        retries_per_model: int = 2,
        max_total_wait: int = 45,
    ) -> str:

        start_time = time.time()
        total_429 = 0

        for model in self.models:
            logger.info(f"Trying model: {model}")

            for attempt in range(retries_per_model):

                if time.time() - start_time > max_total_wait:
                    raise RuntimeError("LLM request timeout")

                self.limiter.wait_if_needed()

                payload = {
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }

                try:
                    response = requests.post(
                        self.BASE_URL,
                        headers=self.headers,
                        json=payload,
                        timeout=60,
                    )

                    data = response.json()

                    if "choices" in data:
                        content = data["choices"][0]["message"]["content"]
                        if content and content.strip():
                            logger.info(f"Success with model: {model}")
                            return content.strip()

                    if "error" in data:
                        if data["error"].get("code") == 429:
                            total_429 += 1
                            logger.warning("429 rate limit received")

                            if total_429 >= 3:
                                raise RuntimeError("Too many 429 responses")

                            self.limiter.trigger_cooldown(20)
                            continue

                except Exception as e:
                    logger.error(f"Request failed: {e}")
                    time.sleep(2)

        raise RuntimeError("All models failed")
