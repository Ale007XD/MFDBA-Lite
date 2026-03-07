import subprocess
import sys
import time
from pathlib import Path


class C:
    GREEN = "\033[92m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"


def c(text, color):
    return f"{color}{text}{C.RESET}"


class TestRunner:

    def __init__(self):
        self.results = []
        self.failed = []

    def run_file(self, path: Path):

        start = time.time()

        try:

            proc = subprocess.run(
                [sys.executable, str(path)]
            )

            duration = time.time() - start

            if proc.returncode == 0:

                print(c("PASS", C.GREEN), path, f"({duration:.3f}s)")
                self.results.append(("PASS", path))

            else:

                print(c("FAIL", C.RED), path)
                self.results.append(("FAIL", path))
                self.failed.append(path)

        except KeyboardInterrupt:
            print(c("\nINTERRUPTED", C.YELLOW))
            sys.exit(1)

    def run_suite(self, tests):

        print(c("──────── MFDBA TEST SUITE ────────", C.CYAN))

        start = time.time()

        for test in tests:
            self.run_file(test)

        duration = time.time() - start

        self.summary(duration)

    def summary(self, duration):

        total = len(self.results)
        passed = sum(1 for r in self.results if r[0] == "PASS")
        failed = total - passed

        print()
        print(c("──────── SUMMARY ────────", C.CYAN))
        print("TOTAL:", total)
        print(c("PASS:", C.GREEN), passed)

        if failed:
            print(c("FAIL:", C.RED), failed)
        else:
            print(c("FAIL:", C.GREEN), 0)

        print(c("TIME:", C.YELLOW), f"{duration:.2f}s")

        if self.failed:

            print()
            print(c("FAILED TESTS:", C.RED))

            for f in self.failed:
                print(" -", f)
