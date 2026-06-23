"""Utility to list all functions and classes in the pydpeet project."""

import ast
import os
from pathlib import Path

import pandas as pd


def get_exported_names(init_file_path: Path = None) -> set[str]:
    """Get the set of exported names from the __init__.py file.

    Args:
        init_file_path: Path to the __init__.py file. Defaults to the main package __init__.py.

    Returns:
        Set of exported names.
    """
    if init_file_path is None:
        # Use relative path from script location to the main package __init__.py
        # Script is at: pydpeet/src/pydpeet/_dev_utils/list_definitions.py
        # We need to go up 2 levels to reach pydpeet/src/pydpeet/__init__.py
        init_file_path = Path(__file__).parent.parent / "__init__.py"
        print(f"DEBUG: __init__.py path: {init_file_path}")
        print(f"DEBUG: Path exists: {init_file_path.exists()}")

    if not init_file_path.exists():
        return set()

    try:
        with open(init_file_path, encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content, filename=str(init_file_path))
        exported_names = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and not node.module.startswith("."):
                    for alias in node.names:
                        exported_names.add(alias.name)
            elif isinstance(node, ast.Assign):
                # Look for __all__ assignments
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "__all__":
                        if isinstance(node.value, ast.List):
                            for elt in node.value.elts:
                                if isinstance(elt, ast.Str):
                                    exported_names.add(elt.s)
                                elif isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                    exported_names.add(elt.value)

        return exported_names
    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"Warning: Could not parse {init_file_path}: {e}")
        return set()


def get_python_files(src_dir: Path, exclude_dirs: list[str] = None, exclude_files: list[str] = None) -> list[Path]:
    """Get all Python files in the source directory recursively.

    Args:
        src_dir: Source directory to scan.
        exclude_dirs: List of directory names to exclude.
        exclude_files: List of Python file names to exclude.
    """
    if exclude_dirs is None:
        exclude_dirs = []
    if exclude_files is None:
        exclude_files = []

    python_files = []
    for root, dirs, files in os.walk(src_dir):
        # Skip __pycache__, hidden directories, and excluded directories
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__" and d not in exclude_dirs]

        for file in files:
            if file.endswith(".py") and file not in exclude_files:
                python_files.append(Path(root) / file)
    return python_files


def extract_definitions(file_path: Path) -> tuple[list[dict], list[dict]]:
    """Extract function and class definitions from a Python file."""
    functions = []
    classes = []

    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content, filename=str(file_path))

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Get function info
                args = [arg.arg for arg in node.args.args]
                functions.append(
                    {
                        "name": node.name,
                        "line": node.lineno,
                        "args": args,
                        "docstring": ast.get_docstring(node),
                    }
                )
            elif isinstance(node, ast.ClassDef):
                # Get class methods
                methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        methods.append(item.name)

                classes.append(
                    {
                        "name": node.name,
                        "line": node.lineno,
                        "methods": methods,
                        "docstring": ast.get_docstring(node),
                    }
                )
    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"Warning: Could not parse {file_path}: {e}")

    return functions, classes


def list_all_definitions(
    src_dir: Path = None, exclude_dirs: list[str] = None, exclude_files: list[str] = None
) -> dict[str, dict]:
    """
    List all functions and classes in the pydpeet project.

    Args:
        src_dir: Path to the source directory. Defaults to pydpeet/src.
        exclude_dirs: List of directory names to exclude.
        exclude_files: List of Python file names to exclude.

    Returns:
        Dictionary mapping file paths to their functions and classes.
    """
    if src_dir is None:
        # Default to pydpeet/src directory
        # Script is at: pydpeet/src/pydpeet/_dev_utils/list_definitions.py
        # We need to go up 3 levels to reach pydpeet/src
        src_dir = Path(__file__).parent.parent.parent

    if exclude_dirs is None:
        exclude_dirs = ["_dev_utils", "citations", "res"]  # Default exclude _dev_utils, citations, and res
    if exclude_files is None:
        exclude_files = []  # Default no file exclusions

    if not src_dir.exists():
        raise FileNotFoundError(f"Source directory not found: {src_dir}")

    python_files = get_python_files(src_dir, exclude_dirs, exclude_files)
    results = {}

    for file_path in python_files:
        # Get relative path from src_dir
        rel_path = file_path.relative_to(src_dir)
        functions, classes = extract_definitions(file_path)

        if functions or classes:
            results[str(rel_path)] = {
                "functions": functions,
                "classes": classes,
            }

    return results


def print_definitions(results: dict[str, dict], show_docstrings: bool = False, check_exports: bool = False) -> None:
    """
    Print all functions and classes in a pandas DataFrame.

    Args:
        results: Dictionary from list_all_definitions.
        show_docstrings: Whether to include docstrings in the output.
        check_exports: Whether to check if items are exported in __init__.py.
    """
    # Get exported names if requested
    exported_names = get_exported_names() if check_exports else set()

    # Collect all items into a list for DataFrame
    items = []

    for file_path, data in results.items():
        functions = data["functions"]
        classes = data["classes"]

        # Add classes
        for cls in classes:
            is_private = cls["name"].startswith("_")
            category = "PRIVATE" if is_private else "OPEN"

            # Add the class itself
            is_exported = check_exports and cls["name"] in exported_names
            items.append(
                {
                    "Category": category,
                    "_type": "CLASS",
                    "Name": cls["name"],
                    "File": file_path,
                    "Line": cls["line"],
                    "Exported": "YES" if is_exported else "NO",
                }
            )

            # Add class methods as functions
            for method_name in cls["methods"]:
                method_is_private = method_name.startswith("_")
                method_category = "PRIVATE" if method_is_private else "OPEN"
                is_exported = check_exports and method_name in exported_names
                items.append(
                    {
                        "Category": method_category,
                        "_type": "FUNCT",
                        "Name": f"{cls['name']}.{method_name}",
                        "File": file_path,
                        "Line": cls["line"],  # Class line number (method lines not tracked)
                        "Exported": "YES" if is_exported else "NO",
                    }
                )

        # Add standalone functions
        for func in functions:
            is_private = func["name"].startswith("_")
            category = "PRIVATE" if is_private else "OPEN"
            is_exported = check_exports and func["name"] in exported_names

            items.append(
                {
                    "Category": category,
                    "_type": "FUNCT",
                    "Name": func["name"],
                    "File": file_path,
                    "Line": func["line"],
                    "Exported": "YES" if is_exported else "NO",
                }
            )

    # Create DataFrame
    df = pd.DataFrame(items)

    if df.empty:
        print("No functions or classes found.")
        return

    # Define custom sort order: OPEN CLASS, OPEN FUNCT, PRIVATE CLASS, PRIVATE FUNCT
    category_order = {"OPEN": 0, "PRIVATE": 1}
    type_order = {"CLASS": 0, "FUNCT": 1}
    df["_sort_key"] = df["Category"].map(category_order) * 2 + df["_type"].map(type_order)

    # Add export priority: YES (0) before NO (1) if Exported column exists
    if "Exported" in df.columns:
        export_order = {"YES": 0, "NO": 1}
        df["_export_key"] = df["Exported"].map(export_order)
        # Sort by sort key, then export status, then File, then Line
        df = (
            df.sort_values(["_sort_key", "_export_key", "File", "Line"])
            .drop(columns=["_sort_key", "_type", "_export_key"])
            .reset_index(drop=True)
        )
    else:
        # Sort by sort key, then File, then Line (no export column)
        df = df.sort_values(["_sort_key", "File", "Line"]).drop(columns=["_sort_key", "_type"]).reset_index(drop=True)

    # Reorder columns to put Exported column last if it exists
    if "Exported" in df.columns:
        cols = [col for col in df.columns if col != "Exported"] + ["Exported"]
        df = df[cols]

    # Configure pandas to display all rows and columns
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)

    # Print the DataFrame
    print(df)

    # Print summary
    print(f"\n{'=' * 80}")
    print("Summary:")
    print(f"  [OPEN] {len(df[df['Category'] == 'OPEN'])} items")
    print(f"  [PRIVATE] {len(df[df['Category'] == 'PRIVATE'])} items")
    print(f"  Total: {len(df)} items across {len(results)} files")

    if check_exports and "Exported" in df.columns:
        exported_count = len(df[df["Exported"] == "YES"])
        print(f"  [EXPORTED] {exported_count} items")
        print(f"  [NOT EXPORTED] {len(df) - exported_count} items")

    print("=" * 80)


def main():
    """Main entry point for the utility."""
    import argparse

    # Always show the path being used for debugging
    init_path = Path(__file__).parent.parent / "__init__.py"
    print(f"DEBUG: __init__.py path would be: {init_path}")
    print(f"DEBUG: Path exists: {init_path.exists()}")
    print()

    parser = argparse.ArgumentParser(description="List all functions and classes in the pydpeet project")
    parser.add_argument("--src-dir", type=Path, help="Path to the source directory (default: pydpeet/src)")
    parser.add_argument(
        "--exclude-dirs",
        nargs="*",
        default=["_dev_utils", "citations", "res"],
        help="List of directory names to exclude (default: _dev_utils, citations, res)",
    )
    parser.add_argument(
        "--exclude-files",
        nargs="*",
        default=["average.py"],
        help="List of Python file names to exclude (default: average.py)",
    )
    parser.add_argument("--docstrings", action="store_true", help="Include docstrings in the output")
    parser.add_argument(
        "--no-check-exports", action="store_true", help="Disable checking if items are exported in __init__.py"
    )

    args = parser.parse_args()

    results = list_all_definitions(args.src_dir, args.exclude_dirs, args.exclude_files)
    print_definitions(results, show_docstrings=args.docstrings, check_exports=not args.no_check_exports)


if __name__ == "__main__":
    main()
    print()
