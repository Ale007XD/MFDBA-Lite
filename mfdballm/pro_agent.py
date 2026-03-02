import sys
from mfdballm.llm_client import LLMClient


def run_agent(task: str) -> str:

    client = LLMClient()

    messages = [
        {"role": "system", "content": "You are a senior software engineer. Return only code."},
        {"role": "user", "content": task},
    ]

    response = client.chat(messages)

    if response.startswith("```"):
        lines = response.split("\n")
        response = "\n".join(lines[1:-1])

    return response.strip()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m mfdballm.pro_agent \"task\"")
        exit(1)

    print(run_agent(sys.argv[1]))
