import os
import requests
import time
import json
import sys

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    print("OPENROUTER_API_KEY not set")
    sys.exit(1)

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://localhost",
    "X-Title": "MFDBA-Pro-Agent"
}

# 🔥 Free models fallback chain
MODELS = [
    "google/gemma-3-12b-it:free",
    "google/gemma-3-4b-it:free",
    "liquid/lfm-2.5-1.2b-instruct:free"
]

SYSTEM_PROMPT = "You are a senior software engineer. Return only valid code. No explanations."


def ask_llm(messages, retries=2):
    for model in MODELS:
        for attempt in range(retries):
            try:
                payload = {
                    "model": model,
                    "messages": messages,
                    "temperature": 0.2,
                    "max_tokens": 1500
                }

                r = requests.post(
                    BASE_URL,
                    headers=HEADERS,
                    json=payload,
                    timeout=60
                )

                data = r.json()

                if "choices" in data:
                    print(f"[OK] Model used: {model}")
                    return data["choices"][0]["message"]["content"]

                if "error" in data:
                    print(f"[MODEL FAIL] {model}: {data['error'].get('message')}")
                    break

            except Exception as e:
                print(f"[RETRY] {model}: {e}")
                time.sleep(2)

    raise Exception("All models failed")


def run_agent(task):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": task}
    ]

    response = ask_llm(messages)

    # Очистка markdown-кода если модель вернула ```python
    if response.startswith("```"):
        response = response.strip("`")
        lines = response.split("\n")
        if lines[0].startswith("python"):
            lines = lines[1:]
        response = "\n".join(lines)

    return response


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pro_agent.py \"your task here\"")
        sys.exit(1)

    task = sys.argv[1]

    print("\n[AGENT START]\n")
    result = run_agent(task)

    print("\n[RESULT]\n")
    print(result)
