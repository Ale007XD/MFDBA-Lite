import subprocess
import sys
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed


TESTS = [
    "tests/provider_response_test.py",
    "tests/tool_executor_test.py",
    "tests/execution_engine_test.py",
    "tests/parser_models_integration_test.py",
    "tests/runtime_loop_safety_test.py",
    "tests/execution_trace_test.py",
    "tests/provider_capabilities_test.py",
]


class Color:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"


def run_test(test):

    start = time.perf_counter()

    result = subprocess.run(
        [sys.executable, test],
        capture_output=True,
        text=True,
    )

    elapsed = time.perf_counter() - start

    return {
        "test": test,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "time": elapsed,
    }


def run(workers=None):

    if workers is None:
        workers = min(len(TESTS), os.cpu_count() or 2)

    suite_start = time.perf_counter()

    print(f"{Color.BLUE}=== MFDBA-Lite Regression Suite ==={Color.RESET}")
    print(f"Workers: {workers}\n")

    failed = False

    with ThreadPoolExecutor(max_workers=workers) as executor:

        futures = {executor.submit(run_test, t): t for t in TESTS}

        for future in as_completed(futures):

            result = future.result()

            test = result["test"]
            elapsed = result["time"]

            if result["stdout"]:
                print(result["stdout"], end="")

            if result["stderr"]:
                print(result["stderr"], end="")

            if result["returncode"] == 0:

                print(
                    f"{Color.GREEN}OK{Color.RESET} "
                    f"{test} ({elapsed:.3f}s)\n"
                )

            else:

                print(
                    f"{Color.RED}FAILED{Color.RESET} "
                    f"{test} ({elapsed:.3f}s)\n"
                )

                failed = True

    total = time.perf_counter() - suite_start

    if failed:

        print(
            f"{Color.RED}TEST SUITE FAILED{Color.RESET} "
            f"(total {total:.3f}s)"
        )

        sys.exit(1)

    print(
        f"{Color.GREEN}ALL TESTS PASSED{Color.RESET} "
        f"(total {total:.3f}s)"
    )


if __name__ == "__main__":

    workers = None

    if "--workers" in sys.argv:

        idx = sys.argv.index("--workers")

        workers = int(sys.argv[idx + 1])

    run(workers)
