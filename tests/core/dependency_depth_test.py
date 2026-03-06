import ast
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = PROJECT_ROOT / "mfdballm"


LAYER_RULES = {
    "router": {"providers", "execution", "types", "models"},
    "execution": {"tools", "types", "models"},
    "tools": {"types", "models"},
    "providers": {"types", "models"},
    "models": set(),
}


def detect_layer(path: Path):

    parts = path.parts

    for layer in LAYER_RULES.keys():
        if layer in parts:
            return layer

    return None


def parse_imports(file_path):

    with open(file_path, "r") as f:
        tree = ast.parse(f.read())

    imports = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):
            for name in node.names:
                imports.append(name.name)

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return imports


def extract_target_layer(import_name):

    if not import_name.startswith("mfdballm"):
        return None

    parts = import_name.split(".")

    if len(parts) < 2:
        return None

    return parts[1]


def collect_python_files():

    return list(SRC_ROOT.rglob("*.py"))


def main():

    files = collect_python_files()

    for file_path in files:

        layer = detect_layer(file_path)

        if layer is None:
            continue

        imports = parse_imports(file_path)

        allowed = LAYER_RULES[layer]

        for imp in imports:

            target_layer = extract_target_layer(imp)

            if target_layer is None:
                continue

            if target_layer == layer:
                continue

            if target_layer not in allowed:
                raise AssertionError(
                    f"\nDependency violation:\n"
                    f"{file_path}\n"
                    f"Layer: {layer}\n"
                    f"Imports: {imp}\n"
                    f"Target layer: {target_layer}\n"
                    f"Allowed: {allowed}\n"
                )

    print("DEPENDENCY DEPTH TEST PASSED")


if __name__ == "__main__":
    main()
