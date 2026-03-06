import os
from pathlib import Path
from test_runner import TestRunner


FAST_FOLDERS = [
    "core",
    "execution",
    "provider",
    "router",
    "tools"
]


def discover_tests():

    tests = []

    for folder in FAST_FOLDERS:

        path = Path("tests") / folder

        for file in path.glob("*_test.py"):
            tests.append(file)

    tests.sort()

    return tests


def main():

    tests = discover_tests()

    print(f"Fast mode: {len(tests)} tests\n")

    runner = TestRunner()

    runner.run_suite(tests)


if __name__ == "__main__":
    main()
