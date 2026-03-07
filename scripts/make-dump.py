#!/usr/bin/env python3

import json
import hashlib
import datetime
import re
from pathlib import Path

PROJECT_ROOT = Path.cwd()

OUTPUT_DIR = Path.home() / "storage/downloads/MFDBA-LLM-Snapshots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

MD_FILE = OUTPUT_DIR / f"snapshot-{TIMESTAMP}.md"
JSON_FILE = OUTPUT_DIR / f"snapshot-{TIMESTAMP}.json"

MAX_FILE_SIZE = 2 * 1024 * 1024

# ─────────────────────────────────────────────
# FILTER CONFIG
# ─────────────────────────────────────────────

ALLOWED_EXT = {
    ".py", ".toml", ".json", ".yaml", ".yml",
    ".md", ".txt", ".sh"
}

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    "venv",
    ".venv",
    "dist",
    "build",
    ".cache",
    ".pytest_cache",
    ".mypy_cache",
    ".tox",
    "htmlcov",
    "scripts"
}

SECRET_NAMES = {
    ".env"
}

SECRET_EXT = {
    ".key", ".pem", ".token", ".secret", ".lock"
}

# ─────────────────────────────────────────────
# SECRET REDACTION
# ─────────────────────────────────────────────

REDACTED = "***REDACTED***"
REDACTED_SECRET = "***REDACTED_SECRET***"

SECRET_KEYS = {
    "password",
    "passwd",
    "secret",
    "token",
    "api_key",
    "apikey",
    "access_key",
    "private_key",
    "client_secret",
    "authorization",
    "auth_token",
    "bearer",
    "jwt",
    "cookie",
    "session"
}

# Known secret patterns
SECRET_PATTERNS = [
    r"sk-[A-Za-z0-9]{20,}",          # OpenAI
    r"ghp_[A-Za-z0-9]{20,}",         # GitHub
    r"AKIA[0-9A-Z]{16}",             # AWS
    r"sk_live_[A-Za-z0-9]{10,}",     # Stripe
    r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",  # JWT
]


def redact_secrets(text: str) -> str:

    # redact config keys

    for key in SECRET_KEYS:

        pattern_json = re.compile(
            rf'("{key}"\s*:\s*)"([^"]+)"',
            re.IGNORECASE
        )

        text = pattern_json.sub(rf'\1"{REDACTED}"', text)

        pattern_env = re.compile(
            rf'({key}\s*=\s*)(.+)',
            re.IGNORECASE
        )

        text = pattern_env.sub(rf'\1{REDACTED}', text)

    # pattern scanning

    for pattern in SECRET_PATTERNS:

        text = re.sub(pattern, REDACTED_SECRET, text)

    return text


# ─────────────────────────────────────────────
# FILE HELPERS
# ─────────────────────────────────────────────

def is_binary(path: Path) -> bool:

    try:
        with path.open("rb") as f:
            chunk = f.read(8192)
            return b"\0" in chunk
    except Exception:
        return True


def sha256(path: Path) -> str:

    h = hashlib.sha256()

    with path.open("rb") as f:

        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)

    return h.hexdigest()


def should_skip(path: Path):

    if path.name in SECRET_NAMES:
        return True

    if path.suffix in SECRET_EXT:
        return True

    for part in path.parts:
        if part in EXCLUDED_DIRS:
            return True

    if path.suffix not in ALLOWED_EXT:
        return True

    return False


# ─────────────────────────────────────────────
# FILE COLLECTION
# ─────────────────────────────────────────────

def collect_files():

    files = []

    for path in PROJECT_ROOT.rglob("*"):

        if not path.is_file():
            continue

        if should_skip(path):
            continue

        files.append(path)

    files.sort()

    return files


# ─────────────────────────────────────────────
# PROJECT TREE
# ─────────────────────────────────────────────

def build_tree():

    lines = []

    for root, dirs, files in PROJECT_ROOT.walk():

        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        root_path = Path(root)

        level = root_path.relative_to(PROJECT_ROOT).parts

        indent = "  " * len(level)

        name = "." if root_path == PROJECT_ROOT else root_path.name

        lines.append(f"{indent}{name}/")

        for f in sorted(files):

            p = root_path / f

            if should_skip(p):
                continue

            lines.append(f"{indent}  {f}")

    return "\n".join(lines)


# ─────────────────────────────────────────────
# FILE READ
# ─────────────────────────────────────────────

def read_file(path: Path):

    size = path.stat().st_size

    if size > MAX_FILE_SIZE:
        return "[file too large]"

    if is_binary(path):
        return "[binary skipped]"

    try:

        content = path.read_text("utf-8")

        content = redact_secrets(content)

        return content

    except Exception:
        return "[read error]"


def language(ext: str):

    return {
        ".py": "python",
        ".json": "json",
        ".toml": "toml",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".sh": "bash",
        ".md": "markdown"
    }.get(ext, "text")


# ─────────────────────────────────────────────
# MARKDOWN SNAPSHOT
# ─────────────────────────────────────────────

def generate_markdown(files):

    with MD_FILE.open("w", encoding="utf-8") as md:

        md.write("# MFDBA-Lite Snapshot\n\n")

        md.write(f"## {datetime.datetime.now()}\n")
        md.write(f"## {PROJECT_ROOT}\n")
        md.write(f"## Files: {len(files)}\n\n")

        md.write("### Project Structure\n")

        md.write("```\n")
        md.write(build_tree())
        md.write("\n```\n\n")

        md.write("### File Contents\n\n")

        for path in files:

            rel = path.relative_to(PROJECT_ROOT)

            md.write(f"## {rel}\n")

            md.write(f"```{language(path.suffix)}\n")

            md.write(read_file(path))

            md.write("\n```\n\n")

        md.write("---\n")
        md.write(f"Created in Termux • {datetime.datetime.now()}\n")


# ─────────────────────────────────────────────
# JSON SNAPSHOT
# ─────────────────────────────────────────────

def generate_json(files):

    snapshot = {
        "snapshot": {
            "generated": str(datetime.datetime.now()),
            "directory": str(PROJECT_ROOT),
            "total_files": len(files),
            "files": []
        }
    }

    for path in files:

        rel = str(path.relative_to(PROJECT_ROOT))

        snapshot["snapshot"]["files"].append({
            "path": rel,
            "size": path.stat().st_size,
            "sha256": sha256(path),
            "content": read_file(path)
        })

    with JSON_FILE.open("w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():

    print("🔍 Scanning project...")

    files = collect_files()

    print(f"📄 Files found: {len(files)}")

    print("📝 Generating Markdown snapshot...")
    generate_markdown(files)

    print("🧾 Generating JSON snapshot...")
    generate_json(files)

    print("\n✅ Snapshot created:\n")

    print(MD_FILE)
    print(JSON_FILE)


if __name__ == "__main__":
    main()
