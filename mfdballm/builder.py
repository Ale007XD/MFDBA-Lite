from mfdballm.orchestrator import Orchestrator


def build(spec_file: str, overwrite=False):
    orch = Orchestrator()
    orch.build(spec_file, overwrite)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m mfdballm.builder spec.json [--force]")
        exit(1)

    spec = sys.argv[1]
    overwrite = "--force" in sys.argv

    build(spec, overwrite)
