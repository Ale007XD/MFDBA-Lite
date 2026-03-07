import subprocess
import sys
import time
import os
from pathlib import Path


FAST_TESTS = [
    "tests/execution/execution_engine_test.py",
    "tests/execution/execution_engine_tool_loop_test.py",
    "tests/execution/tool_loop_limit_test.py",
    "tests/execution/execution_step_builder_test.py",

    "tests/tools/tool_executor_test.py",
    "tests/tools/tool_executor_result_test.py",

    "tests/provider/provider_response_test.py",

    "tests/runtime/runtime_loop_safety_test.py",
]


SEPARATOR = "────────────────────────────────"


def run_test(test_path: str, index: int, total: int) -> bool:
    print()
    print(SEPARATOR)
    print(f"[{index}/{total}] RUN {test_path}")
    print(SEPARATOR)

    start = time.time()

    result = subprocess.run(
        [sys.executable, test_path],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

    duration = time.time() - start

    if result.returncode != 0:
        print(f"\n❌ FAIL {test_path} ({duration:.2f}s)")
        return False

    print(f"\n✅ PASS {test_path} ({duration:.2f}s)")
    return True


def main():
    project_root = Path(__file__).resolve().parent.parent

    if Path.cwd() != project_root:
        print(f"Switching to project root: {project_root}")
        os.chdir(project_root)

    total = len(FAST_TESTS)
    passed = 0

    print()
    print("⚡ MFDBA FAST TEST SUITE")
    print(SEPARATOR)
    print(f"Running {total} critical tests\n")

    start_suite = time.time()

    for i, test in enumerate(FAST_TESTS, start=1):
        ok = run_test(test, i, total)

        if not ok:
            print()
            print("❌ FAST TEST SUITE FAILED")
            sys.exit(1)

        passed += 1

    total_time = time.time() - start_suite

    print()
    print(SEPARATOR)
    print("🎉 ALL FAST TESTS PASSED")
    print(SEPARATOR)
    print(f"Passed: {passed}/{total}")
    print(f"Total time: {total_time:.2f}s")
    print(SEPARATOR)


if __name__ == "__main__":
    main()
