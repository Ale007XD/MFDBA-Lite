import argparse
from .orchestrator_llm import ask_llm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="User prompt")
    args = parser.parse_args()

    result = ask_llm(
        "You are a precise coding assistant.",
        args.prompt
    )

    print(result)
