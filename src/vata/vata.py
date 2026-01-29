# vata.py — Serious + legacy fun mode in one standalone file
# Run directly: python vata.py check yourfile.py --verbose
# No pip install needed

import argparse
import sys
import ast
from pathlib import Path


def simple_complexity_estimate(code: str) -> int:
    """Very basic cyclomatic complexity approximation without external libs."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return -1  # invalid code

    complexity = 1
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.While, ast.For, ast.Try, ast.ExceptHandler)):
            complexity += 1
        elif isinstance(node, ast.BoolOp):
            complexity += len(node.values) - 1
    return complexity


def analyze_code(file_path: str, verbose: bool = False) -> None:
    """Serious code quality check using only stdlib + ast."""
    path = Path(file_path)
    if not path.is_file():
        print(f"Error: Not a file → {file_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with path.open(encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    lines = code.splitlines()
    loc = len(lines)
    blank_lines = sum(1 for line in lines if not line.strip())
    comment_lines = sum(1 for line in lines if line.strip().startswith("#"))
    comment_ratio = (comment_lines / loc * 100) if loc > 0 else 0

    complexity = simple_complexity_estimate(code)

    print(f"\nAnalysis of: {file_path}")
    print("─" * 60)
    print(f"Lines of code (LOC)       : {loc}")
    print(f"Blank lines               : {blank_lines} ({blank_lines/loc*100:.1f}%)")
    print(f"Comment lines             : {comment_lines} ({comment_ratio:.1f}%)")
    print(f"Estimated complexity      : {complexity if complexity >= 0 else 'Syntax error'}")

    if verbose:
        print("\nQuick notes:")
        if loc > 300:
            print("  • File is quite long — consider splitting into smaller modules")
        if comment_ratio < 10:
            print("  • Low comment ratio — add more explanations")
        if complexity > 15:
            print("  • High complexity — consider refactoring deeply nested code")

    print(f"\nOverall quality impression: {'Good' if complexity <= 15 and comment_ratio >= 10 else 'Needs work'}")
    print("")


def legacy_humanize(file_path: str) -> None:
    """Placeholder for the old fun mode — you can expand later."""
    print(f"Legacy humanize mode on: {file_path}")
    print("─" * 60)
    print("HUMANIZED VERSION (demo):")
    print("# rage mode activated frfr 😂")
    print("def sigma_function(rizz): return 'ngmi' if not rizz else 'based af'")
    print("SOUL SCORE: 98/100 (close but ngmi)")
    print("")


def main():
    parser = argparse.ArgumentParser(
        prog="vata",
        description="VATA — Serious code quality checker (standalone)"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Serious check
    check_parser = subparsers.add_parser("check", help="Analyze code quality")
    check_parser.add_argument("file", help="Python file to check")
    check_parser.add_argument("--verbose", action="store_true", help="More details")

    # Legacy fun mode
    human_parser = subparsers.add_parser("humanize", help="Old meme humanizer mode")
    human_parser.add_argument("file", help="File to humanize")

    args = parser.parse_args()

    if args.command == "check":
        analyze_code(args.file, args.verbose)
    elif args.command == "humanize":
        legacy_humanize(args.file)


if __name__ == "__main__":
    main()
