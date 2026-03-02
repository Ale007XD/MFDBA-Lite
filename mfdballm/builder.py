import os
import json
import time
import requests
from pathlib import Path

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

MODELS = [
    "google/gemma-3-12b-it:free",
    "google/gemma-3-4b-it:free",
    "nvidia/nemotron-nano-9b-v2:free",
]

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

SYSTEM_PLANNER = """You are a senior software architect.
Break the task into JSON array:
[
  {"path": "relative/path/file.ext", "description": "what to generate"}
]
Return ONLY valid JSON.
"""

SYSTEM_EXECUTOR = """You are a senior backend engineer.
Generate full file content.
Return ONLY raw code.
No explanations.
"""

# ================= LLM CALL =================

def ask_llm(instruction, user_content, max_tokens=2000):

    for model in MODELS:

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": instruction + "\n\n" + user_content
                }
            ],
            "temperature": 0.2,
            "max_tokens": max_tokens
        }

        try:
            print(f"[LLM] {model}")
            r = requests.post(BASE_URL, headers=HEADERS, json=payload, timeout=90)
            data = r.json()

            if "choices" in data:
                content = data["choices"][0]["message"]["content"]
                if content.strip():
                    return content

            print("[FAILED MODEL]", data)

        except Exception as e:
            print("[ERROR]", e)

        time.sleep(2)

    raise Exception("All models failed")

# ================= HELPERS =================

def extract_json(text):
    text = text.strip()

    # remove markdown fences
    if "```" in text:
        text = text.split("```")[1]

    # find first [ and last ]
    start = text.find("[")
    end = text.rfind("]")

    if start != -1 and end != -1:
        return text[start:end+1]

    return text

# ================= BUILDER =================

def plan_repository(spec_text):
    print("[PLANNER]")
    raw = ask_llm(SYSTEM_PLANNER, spec_text, max_tokens=1500)
    cleaned = extract_json(raw)

    try:
        return json.loads(cleaned)
    except:
        print("Invalid JSON from model:\n", raw)
        raise

def generate_file(file_path, description, spec_text, overwrite=False):
    path = Path(file_path)

    if path.exists() and not overwrite:
        print(f"[SKIP] {file_path}")
        return

    print(f"[GEN] {file_path}")

    prompt = f"""
Project spec:
{spec_text}

File:
{file_path}

Description:
{description}
"""

    content = ask_llm(SYSTEM_EXECUTOR, prompt, max_tokens=3000)

    if content.startswith("```"):
        lines = content.split("\n")
        content = "\n".join(lines[1:-1])

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)

def build(spec_file, overwrite=False):
    spec_text = Path(spec_file).read_text()
    plan = plan_repository(spec_text)

    for item in plan:
        generate_file(
            item["path"],
            item["description"],
            spec_text,
            overwrite
        )
        time.sleep(1)

    print("\n[BUILD COMPLETE]")

# ================= ENTRY =================

if __name__ == "__main__":
    import sys

    if not API_KEY:
        print("Set OPENROUTER_API_KEY first")
        exit(1)

    if len(sys.argv) < 2:
        print("Usage: python builder.py spec.json [--force]")
        exit(1)

    spec_path = sys.argv[1]
    overwrite = "--force" in sys.argv

    build(spec_path, overwrite)
