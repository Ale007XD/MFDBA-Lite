import ast
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = PROJECT_ROOT / "mfdballm"


def get_imports(file_path):
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())

    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name)

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return imports


def collect_python_files(path):
    return list(path.rglob("*.py"))


def check_router_rules(file_path, imports):

    for imp in imports:
        if "tools" in imp:
            raise AssertionError(
                f"Router must not import tools: {file_path} -> {imp}"
            )


def check_provider_rules(file_path, imports):

    for imp in imports:
        if "tools" in imp:
            raise AssertionError(
                f"Provider must not import tools: {file_path} -> {imp}"
            )

        if "execution" in imp:
            raise AssertionError(
                f"Provider must not import execution: {file_path} -> {imp}"
            )


def check_tools_rules(file_path, imports):

    for imp in imports:
        if "providers" in imp:
            raise AssertionError(
                f"Tools must not import providers: {file_path} -> {imp}"
            )


def main():

    router_dir = SRC_ROOT / "router"
    providers_dir = SRC_ROOT / "providers"
    tools_dir = SRC_ROOT / "tools"

    # Router rules
    if router_dir.exists():
        for f in collect_python_files(router_dir):
            imports = get_imports(f)
            check_router_rules(f, imports)

    # Provider rules
    if providers_dir.exists():
        for f in collect_python_files(providers_dir):
            imports = get_imports(f)
            check_provider_rules(f, imports)

    # Tools rules
    if tools_dir.exists():
        for f in collect_python_files(tools_dir):
            imports = get_imports(f)
            check_tools_rules(f, imports)

    print("ARCHITECTURE TEST PASSED")


if __name__ == "__main__":
    main()
