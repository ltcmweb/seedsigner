import ast
import sys
from pathlib import Path


def extract_sections(source: str):
    """
    Returns:
        header: str
        classes: list[tuple[str, str]]
            [(class_name, class_source), ...]
    """

    tree = ast.parse(source)

    # Top-level class definitions only
    class_nodes = [
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    ]

    lines = source.splitlines(keepends=True)

    if not class_nodes:
        return source, []

    # Everything before first class
    first_class = class_nodes[0]

    if first_class.decorator_list:
        first_line = first_class.decorator_list[0].lineno
    else:
        first_line = first_class.lineno

    header = "".join(lines[: first_line - 1])

    classes = []

    for i, node in enumerate(class_nodes):
        if node.decorator_list:
            start = node.decorator_list[0].lineno - 1
        else:
            start = node.lineno - 1

        if i + 1 < len(class_nodes):
            next_node = class_nodes[i + 1]

            if next_node.decorator_list:
                end = next_node.decorator_list[0].lineno - 1
            else:
                end = next_node.lineno - 1
        else:
            end = len(lines)

        class_source = "".join(lines[start:end])
        classes.append((node.name, class_source))

    return header, classes


def rewrite_imports(header: str) -> str:
    return header.replace(
        "from .screen import",
        "from seedsigner.gui.screens.screen import",
    )


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 generator.py <file.py>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    source = input_path.read_text(encoding="utf-8")

    header, classes = extract_sections(source)

    # Rewrite imports here
    header = rewrite_imports(header)

    output_dir = Path("generated")
    output_dir.mkdir(parents=True, exist_ok=True)

    for class_name, class_source in classes:
        output_path = output_dir / f"{class_name}.py"

        content = header.rstrip() + "\n\n" + class_source

        output_path.write_text(content, encoding="utf-8")

        print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
