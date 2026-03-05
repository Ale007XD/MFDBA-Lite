import os
import time

from mfdballm.provider_registry import build_providers
from mfdballm.router import Router


def run_live_test():

    print("\n=== MFDBA LIVE SYSTEM TEST ===\n")

    providers = build_providers()

    print("Loaded providers:")
    for p in providers:
        print(" -", p.name)

    router = Router(providers)

    message = [{"role": "user", "content": "Say hello in one short sentence"}]

    print("\n--- Chat test ---")

    try:
        result = router.chat(message, timeout=30)

        print("\nMODEL RESPONSE:")
        print(result)

    except Exception as e:
        print("\nRouter failed:", e)
        return

    print("\n--- Router Health Snapshot ---")

    snapshot = router.get_health_snapshot()

    for s in snapshot:
        print(s)

    print("\n--- Stress test (10 calls) ---")

    for i in range(10):

        try:
            r = router.chat(message, timeout=20)
            print(f"{i+1}: OK")

        except Exception as e:
            print(f"{i+1}: FAIL", e)

        time.sleep(1)

    print("\n--- Final Snapshot ---")

    snapshot = router.get_health_snapshot()

    for s in snapshot:
        print(s)

    print("\n=== TEST COMPLETE ===\n")


if __name__ == "__main__":
    run_live_test()
