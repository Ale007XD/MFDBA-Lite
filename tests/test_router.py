import unittest

from mfdballm.router import Router
from mfdballm.providers.base import BaseProvider


class HealthyProvider(BaseProvider):
    def __init__(self):
        super().__init__("healthy")

    def chat(self, messages):
        return "OK"

    def health(self):
        return True


class FailingProvider(BaseProvider):
    def __init__(self):
        super().__init__("failing")

    def chat(self, messages):
        raise RuntimeError("Failure")

    def health(self):
        return True


class UnhealthyProvider(BaseProvider):
    def __init__(self):
        super().__init__("unhealthy")

    def chat(self, messages):
        return "SHOULD NOT RUN"

    def health(self):
        return False


class RouterTest(unittest.TestCase):

    def test_fallback(self):
        router = Router([FailingProvider(), HealthyProvider()])
        result = router.chat([{"role": "user", "content": "hi"}])
        self.assertEqual(result, "OK")

    def test_skip_unhealthy(self):
        router = Router([UnhealthyProvider(), HealthyProvider()])
        result = router.chat([{"role": "user", "content": "hi"}])
        self.assertEqual(result, "OK")

    def test_all_fail(self):
        router = Router([FailingProvider()])
        with self.assertRaises(RuntimeError):
            router.chat([{"role": "user", "content": "hi"}])


if __name__ == "__main__":
    unittest.main()
