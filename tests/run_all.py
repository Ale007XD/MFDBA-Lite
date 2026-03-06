import os
from pathlib import Path
from test_runner import TestRunner


TEST_ROOT = Path("tests")


def discover_tests():

    tests = []

    for root, dirs, files in os.walk(TEST_ROOT):

        for file in files:

            if not file.endswith("_test.py"):
                continue

            tests.append(Path(root) / file)

    tests.sort()

    return tests


def main():

    tests = discover_tests()

    print(f"Discovered {len(tests)} tests\n")

    runner = TestRunner()

    runner.run_suite(tests)


if __name__ == "__main__":
    main()
