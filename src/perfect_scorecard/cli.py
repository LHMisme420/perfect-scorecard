import argparse
import sys
import subprocess
from pathlib import Path
from .analyzer import analyze_file, print_analysis

def humanize_file(file_path: str, level: str = "medium", target: int = 75, iterations: int = 5, diff: bool = False):
    """Legacy fun mode - keep as easter egg or remove later"""
    print(f"Humanizing ({level} mode, target {target})...")
    print(f"ORIGINAL:\n{file_path}\n{'─' * 80}")
    
    # Your existing humanization logic here (stubbed for now)
    humanized = "# RAGE ONE-LINER frfr 😂 # sigma 💀\nbasedCounter/ngmiVar.frfrVal"
    soul_score = 98  # fake, replace with real logic if keeping
    
    print(f"HUMANIZED:\n{humanized}\n{'─' * 80}")
    print(f"SOUL SCORE: {soul_score}/100")
    if soul_score >= target:
        print("TARGET REACHED! 🔥")
    else:
        print(f"Score below target ({soul_score} < {target})")
    
    if diff:
        print("DIFF:")
        print("--- original")
        print("+++ humanized")
        print("@@ -1 +1 @@")
        print(f"+{humanized}")
        print(file_path)

def main():
    parser = argparse.ArgumentParser(
        prog="vata",
        description="Python code quality & improvement tool"
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Serious check command
    check_parser = subparsers.add_parser("check", help="Analyze code quality and maintainability")
    check_parser.add_argument("files", nargs="+", type=str, help="Python file(s) or directory")
    check_parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    check_parser.add_argument("--fix", action="store_true", help="Attempt to auto-fix style issues (requires ruff)")

    # Legacy/fun humanize command (can be removed later)
    human_parser = subparsers.add_parser("humanize", help="Apply fun humanization (legacy mode)")
    human_parser.add_argument("file", type=str, help="File to humanize")
    human_parser.add_argument("--level", default="medium", choices=["low", "medium", "high", "rage"],
                              help="Humanization intensity")
    human_parser.add_argument("--target", type=int, default=75, help="Target soul score")
    human_parser.add_argument("--iterations", type=int, default=5, help="Max refinement passes")
    human_parser.add_argument("--diff", action="store_true", help="Show diff")

    args = parser.parse_args()

    if args.command == "check":
        for file_arg in args.files:
            path = Path(file_arg)
            if not path.exists():
                print(f"Error: File/directory not found: {file_arg}", file=sys.stderr)
                continue
            
            if path.is_dir():
                print(f"Scanning directory: {path}")
                for pyfile in path.rglob("*.py"):
                    if pyfile.name.startswith("_"):  # skip private files if desired
                        continue
                    results = analyze_file(str(pyfile))
                    print_analysis(results, verbose=args.verbose)
            else:
                results = analyze_file(str(path))
                print_analysis(results, verbose=args.verbose)
            
            # Optional auto-fix with ruff
            if args.fix:
                try:
                    subprocess.run(["ruff", "check", "--fix", str(path)], check=True)
                    print("Style fixes applied via ruff.")
                except FileNotFoundError:
                    print("Warning: ruff not found. Install with: pip install ruff")
                except subprocess.CalledProcessError:
                    print("ruff fix completed with warnings/errors.")

    elif args.command == "humanize":
        humanize_file(args.file, args.level, args.target, args.iterations, args.diff)

    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
