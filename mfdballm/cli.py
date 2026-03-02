# mfdballm/cli.py

import argparse
import logging
import sys
from pprint import pprint

from mfdballm.llm_client import LLMClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


def main():
    parser = argparse.ArgumentParser(
        description="MFDBA LLM CLI"
    )

    subparsers = parser.add_subparsers(dest="command")

    chat_parser = subparsers.add_parser("chat")
    chat_parser.add_argument("message", type=str)

    subparsers.add_parser("health")
    subparsers.add_parser("doctor")

    args = parser.parse_args()

    client = LLMClient()

    if args.command == "chat":

        messages = [
            {"role": "user", "content": args.message}
        ]

        try:
            result = client.chat(messages)
            print(result)
            return 0
        except Exception as e:
            print(f"ERROR: {e}")
            return 1

    elif args.command == "doctor":

        snapshot = client.router.get_health_snapshot()

        print("\n=== PROVIDER HEALTH STATUS ===\n")

        for provider in snapshot:
            pprint(provider)
            print()

        return 0

    elif args.command == "health":
        print("OK")
        return 0

    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
