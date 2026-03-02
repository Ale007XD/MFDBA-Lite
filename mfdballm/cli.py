import argparse
import logging
import requests
import os

from mfdballm.llm_client import LLMClient
from mfdballm.logging_config import configure_logging


def health_check():
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        print("LLM health: FAIL (API key not set)")
        return

    try:
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=5,
        )

        if response.status_code == 200:
            print("LLM health: OK")
        else:
            print(f"LLM health: FAIL (HTTP {response.status_code})")

    except Exception as e:
        print(f"LLM health: FAIL ({e})")


def main():
    configure_logging()

    parser = argparse.ArgumentParser(prog="mfdballm")
    subparsers = parser.add_subparsers(dest="command")

    chat_parser = subparsers.add_parser("chat")
    chat_parser.add_argument("prompt")

    subparsers.add_parser("health")

    args = parser.parse_args()

    if args.command == "health":
        health_check()
        return

    if args.command == "chat":
        client = LLMClient()

        messages = [
            {"role": "system", "content": "You are a precise coding assistant."},
            {"role": "user", "content": args.prompt},
        ]

        result = client.chat(messages)
        print(result)
        return

    parser.print_help()
