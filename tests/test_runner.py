import importlib.util
import traceback
import time
import sys
from pathlib import Path


class TestRunner:

    def __init__(self):

        self.total = 0
        self.failed = 0

    def run_file(self, path):

        start = time.time()

        try:

            spec = importlib.util.spec_from_file_location("test_module", path)
            module = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(module)

            if hasattr(module, "main"):
                module.main()

            duration = time.time() - start

            print(f"OK {path} ({duration:.3f}s)")

        except Exception:

            duration = time.time() - start

            print(f"FAILED {path} ({duration:.3f}s)")

            traceback.print_exc()

            self.failed += 1

        self.total += 1

    def run_suite(self, tests):

        start = time.time()

        for test in tests:
            self.run_file(test)

        total = time.time() - start

        if self.failed:

            print(f"\nFAILED {self.failed}/{self.total} tests")
            sys.exit(1)

        print(f"\nALL TESTS PASSED ({total:.3f}s)")
