import unittest
from unittest.mock import patch

from mfdballm.router import Router
from mfdballm.providers.base import BaseProvider
from mfdballm.exceptions import ProviderTimeoutError


class TimeoutProvider(BaseProvider):

    def __init__(self):
        super().__init__("timeout")

    def chat(self, messages, timeout=None):
        raise ProviderTimeoutError("simulated timeout")

    def health(self):
        return True


class TimeoutTest(unittest.TestCase):

    def test_timeout(self):

        router = Router([TimeoutProvider()])

        with self.assertRaises(RuntimeError):
            router.chat(
                [{"role": "user", "content": "hello"}],
                timeout=2
            )


if __name__ == "__main__":
    unittest.main()
