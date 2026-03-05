import requests

from mfdballm.config import get_local_models
from mfdballm.exceptions import ProviderUnavailableError
from mfdballm.providers.base import BaseProvider


class LocalProvider(BaseProvider):

    name = "local"

    def __init__(self):

        self.models = get_local_models()

    def chat(self, messages):

        prompt = messages[-1]["content"]

        last_error = None

        for model in self.models:

            try:

                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False,
                    },
                    timeout=60,
                )

                data = response.json()

                return data["response"]

            except Exception as e:

                last_error = e
                continue

        raise ProviderUnavailableError(
            f"All local models failed. Last error: {last_error}"
        )
