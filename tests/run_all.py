import os
import subprocess
from pathlib import Path
from test_runner import TestRunner

TEST_ROOT = Path("tests")


def discover_tests():
    tests = []

    for root, dirs, files in os.walk(TEST_ROOT):
        for file in files:

            if file.endswith("_test.py"):
                tests.append(Path(root) / file)

    tests.sort()
    return tests


def main():

    tests = discover_tests()

    print(f"\033[96mDiscovered {len(tests)} tests\033[0m\n")

    runner = TestRunner()
    runner.run_suite(tests)

    # копирование всего вывода через shell tee
    try:
        subprocess.run(
            "python tests/run_all.py | termux-clipboard-set",
            shell=True
        )
    except Exception:
        pass


if __name__ == "__main__":
    main()
