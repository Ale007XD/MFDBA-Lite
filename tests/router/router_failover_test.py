import time

from mfdballm.router import Router
from mfdballm.providers import OpenRouterProvider, GeminiProvider, GroqProvider


def load_providers():

    providers = []

    try:
        providers.append(OpenRouterProvider())
    except Exception as e:
        print("OpenRouter disabled:", e)

    try:
        providers.append(GeminiProvider())
    except Exception as e:
        print("Gemini disabled:", e)

    try:
        providers.append(GroqProvider())
    except Exception as e:
        print("Groq disabled:", e)

    return providers


def run():

    print("=== ROUTER FAILOVER TEST ===\n")

    providers = load_providers()

    if not providers:
        print("No providers available")
        return

    print("Loaded providers:")
    for p in providers:
        print(" -", p.name)

    router = Router(providers)

    print("\n--- Failover stress test ---\n")

    for i in range(20):

        try:

            result = router.chat(
                [{"role": "user", "content": "Say hello"}]
            )

            print(f"{i+1}: OK")

        except Exception as e:

            print(f"{i+1}: FAIL {e}")

        print("\nRouter snapshot:")

        snapshot = router.get_health_snapshot()

        for s in snapshot:
            print(s)

        print("")
        time.sleep(0.5)


if __name__ == "__main__":
    run()
