import unittest
import time
import os

from mfdballm.router import Router
from mfdballm.providers.base import BaseProvider


# -------------------------------------------------
# Test Providers
# -------------------------------------------------

class AlwaysHealthyProvider(BaseProvider):

    def __init__(self):
        super().__init__("healthy")

    def chat(self, messages, timeout=None):
        return "OK"

    def health(self):
        return True


class AlwaysFailProvider(BaseProvider):

    def __init__(self):
        super().__init__("fail")

    def chat(self, messages, timeout=None):
        raise RuntimeError("provider failure")

    def health(self):
        return True


class FlakyProvider(BaseProvider):
    """
    Fails first N times then succeeds
    """

    def __init__(self, fail_times=2):
        super().__init__("flaky")
        self.counter = 0
        self.fail_times = fail_times

    def chat(self, messages, timeout=None):
        self.counter += 1
        if self.counter <= self.fail_times:
            raise RuntimeError("flaky failure")
        return "RECOVERED"

    def health(self):
        return True


# -------------------------------------------------
# Tests
# -------------------------------------------------

class CircuitBreakerTest(unittest.TestCase):

    def setUp(self):

        os.environ["MFDBA_FAILURE_THRESHOLD"] = "2"
        os.environ["MFDBA_RECOVERY_TIMEOUT"] = "1"
        os.environ["MFDBA_HALF_OPEN_MAX_REQUESTS"] = "1"
        os.environ["MFDBA_MAX_RETRIES"] = "1"

    def tearDown(self):

        for k in [
            "MFDBA_FAILURE_THRESHOLD",
            "MFDBA_RECOVERY_TIMEOUT",
            "MFDBA_HALF_OPEN_MAX_REQUESTS",
            "MFDBA_MAX_RETRIES",
        ]:
            os.environ.pop(k, None)

    # ------------------------------------------

    def test_fallback_to_second_provider(self):

        router = Router([
            AlwaysFailProvider(),
            AlwaysHealthyProvider()
        ])

        result = router.chat([{"role": "user", "content": "hi"}])

        self.assertEqual(result, "OK")

    # ------------------------------------------

    def test_circuit_opens_after_failures(self):

        router = Router([AlwaysFailProvider()])

        for _ in range(2):
            try:
                router.chat([{"role": "user", "content": "hi"}])
            except RuntimeError:
                pass

        snapshot = router.get_health_snapshot()[0]

        self.assertEqual(snapshot["state"], "OPEN")

    # ------------------------------------------

    def test_open_to_half_open_transition(self):

        router = Router([AlwaysFailProvider()])

        for _ in range(2):
            try:
                router.chat([{"role": "user", "content": "hi"}])
            except RuntimeError:
                pass

        time.sleep(1.2)

        state = router.provider_states[0]

        self.assertTrue(state.is_available())
        self.assertEqual(state.state.value, "HALF_OPEN")

    # ------------------------------------------

    def test_half_open_to_closed_on_success(self):

        router = Router([FlakyProvider(fail_times=2)])

        # trip circuit
        for _ in range(2):
            try:
                router.chat([{"role": "user", "content": "hi"}])
            except RuntimeError:
                pass

        time.sleep(1.2)

        result = router.chat([{"role": "user", "content": "hi"}])

        self.assertEqual(result, "RECOVERED")

        snapshot = router.get_health_snapshot()[0]

        self.assertEqual(snapshot["state"], "CLOSED")

    # ------------------------------------------

    def test_half_open_failure_reopens_circuit(self):

        router = Router([AlwaysFailProvider()])

        for _ in range(2):
            try:
                router.chat([{"role": "user", "content": "hi"}])
            except RuntimeError:
                pass

        time.sleep(1.2)

        try:
            router.chat([{"role": "user", "content": "hi"}])
        except RuntimeError:
            pass

        snapshot = router.get_health_snapshot()[0]

        self.assertEqual(snapshot["state"], "OPEN")


if __name__ == "__main__":
    unittest.main()
