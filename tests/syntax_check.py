#!/usr/bin/env python3

import py_compile
import sys
from pathlib import Path


def collect_python_files(root: Path):
    files = []

    for path in root.rglob("*.py"):
        if "__pycache__" in str(path):
            continue
        files.append(path)

    return files


def check_file(file_path: Path):
    try:
        py_compile.compile(file_path, doraise=True)
        return True, None
    except py_compile.PyCompileError as e:
        return False, str(e)


def run_syntax_check():
    project_root = Path(__file__).resolve().parent.parent
    source_root = project_root / "mfdballm"

    files = collect_python_files(source_root)

    print("\n==============================")
    print("Syntax Check")
    print("==============================\n")

    failed = []

    for f in files:
        ok, error = check_file(f)

        if ok:
            print(f"✓ {f}")
        else:
            print(f"✗ {f}")
            print(error)
            failed.append(f)

    if failed:
        print("\n❌ Syntax errors detected")
        return False

    print("\n✅ Syntax check passed")
    return True


if __name__ == "__main__":
    ok = run_syntax_check()
    sys.exit(0 if ok else 1)
