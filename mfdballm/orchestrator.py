import os
import json
import time
import requests
from pathlib import Path
from rate_limiter import RateLimiter

# ================= CONFIG =================

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY not set")

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# SINGLE stable model for IP safety
MODEL = "google/gemma-3-12b-it:free"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://localhost",
    "X-Title": "MFDBA-Orchestrator"
}

SYSTEM_PLANNER = """You are a senior software architect.
Break the task into JSON array of files:
[
  {"path": "relative/path/file.ext", "description": "what to generate"}
]
Return ONLY valid JSON.
"""

SYSTEM_EXECUTOR = """You are a senior backend engineer.
Generate full file content.
Return ONLY raw code or markdown.
No explanations.
"""

# ================= RATE LIMITER =================

limiter = RateLimiter(
    max_requests=8,      # safe free limit
    window_seconds=60,
    min_delay=6          # anti-burst
)

# ================= HELPERS =================

def clean_json(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
    return raw.strip()


def ask_llm(system_prompt, user_prompt, max_tokens=2000, retries=5):
    for attempt in range(retries):

        limiter.wait_if_needed()

        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.2,
            "max_tokens": max_tokens
        }

        try:
            print(f"[LLM] attempt {attempt+1}")

            r = requests.post(
                BASE_URL,
                headers=HEADERS,
                json=payload,
                timeout=120
            )

            data = r.json()

            if "choices" in data:
                choice = data["choices"][0]

                if choice.get("finish_reason") == "length":
                    print("[TRUNCATED] retrying with higher token limit")
                    max_tokens += 1000
                    continue

                content = choice["message"]["content"]
                if content and content.strip():
                    return content

            if "error" in data:
                code = data["error"].get("code")

                if code == 429:
                    print("[RATE LIMITED] triggering cooldown")
                    limiter.trigger_cooldown(40)
                    continue

            print("[MODEL ERROR]", data)

        except Exception as e:
            print("[ERROR]", e)
            time.sleep(5)

    raise Exception("LLM failed after retries")


# ================= BUILDER =================

def build(spec_path: str, overwrite=False):
    spec_file = Path(spec_path)

    if not spec_file.exists():
        raise FileNotFoundError(spec_path)

    raw_spec = spec_file.read_text().strip()
    if not raw_spec:
        raise ValueError("project_spec.json is empty")

    spec = json.loads(raw_spec)

    project_name = spec.get("project_name", "AI_Project")
    description = spec.get("description", "")
    requirements = spec.get("requirements", [])

    plan_prompt = f"""
Project: {project_name}

Description:
{description}

Requirements:
{json.dumps(requirements, indent=2)}
"""

    # Planner with small tokens (safe)
    plan_raw = ask_llm(SYSTEM_PLANNER, plan_prompt, max_tokens=1200)
    files = json.loads(clean_json(plan_raw))

    for file in files:
        path = Path(file["path"])
        desc = file["description"]

        if path.exists() and not overwrite:
            print(f"[SKIP] {path}")
            continue

        print(f"[GEN] {path}")

        file_prompt = f"""
Project: {project_name}

File path: {path}

What this file must do:
{desc}

Follow architecture rules strictly.
"""

        content = ask_llm(SYSTEM_EXECUTOR, file_prompt, max_tokens=2500)

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.strip())

        # Anti-burst pause between files
        print("[FILE PAUSE] sleeping 8s")
        time.sleep(8)


# ================= CLI =================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py project_spec.json [--force]")
        exit(1)

    spec_file = sys.argv[1]
    overwrite_flag = "--force" in sys.argv

    build(spec_file, overwrite_flag)
