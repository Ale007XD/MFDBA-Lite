#!/usr/bin/env python3

import subprocess
import sys
import time
from pathlib import Path


def run_step(name, cmd):
    print(f"\n=== {name} ===\n")

    start = time.time()

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    duration = time.time() - start

    print(result.stdout)

    if result.returncode != 0:
        print(f"❌ {name} FAILED ({duration:.2f}s)")
        sys.exit(1)

    print(f"✅ {name} OK ({duration:.2f}s)")


def main():
    project_root = Path(__file__).resolve().parent.parent

    print("\n================================")
    print("MFDBA-Lite Development Runner")
    print("================================")

    total_start = time.time()

    # Step 1 — syntax check
    run_step(
        "Syntax Check",
        [sys.executable, str(project_root / "tests" / "syntax_check.py")],
    )

    # Step 2 — run tests
    run_step(
        "Regression Tests",
        [sys.executable, str(project_root / "tests" / "run_all.py")],
    )

    total_time = time.time() - total_start

    print("\n================================")
    print(f"ALL CHECKS PASSED ✅ ({total_time:.2f}s)")
    print("================================\n")


if __name__ == "__main__":
    main()
