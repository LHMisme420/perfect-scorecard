import radon.raw
import radon.metrics
import radon.complexity
import subprocess
import json
from typing import Dict, Any

def analyze_file(filepath: str) -> Dict[str, Any]:
    """Perform real code quality analysis."""
    results: Dict[str, Any] = {"file": filepath}

    try:
        with open(filepath, encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        results["error"] = str(e)
        return results

    # Raw statistics
    raw = radon.raw.analyze(code)
    results.update({
        "loc": raw.loc,
        "lloc": raw.lloc,
        "sloc": raw.sloc,
        "comments": raw.comments,
        "blank": raw.blank,
    })

    # Maintainability Index (higher = better)
    mi = radon.metrics.mi_visit(code, multi=True)
    results["maintainability_index"] = round(mi, 2)

    # Cyclomatic complexity
    try:
        cc = radon.complexity.cc_visit(code)
        results["cyclomatic_complexity"] = sum(item.complexity for item in cc)
        results["complex_functions"] = len(cc)
    except:
        results["cyclomatic_complexity"] = "error"

    # Ruff check (optional but recommended)
    try:
        ruff = subprocess.run(
            ["ruff", "check", "--output-format=json", filepath],
            capture_output=True, text=True, timeout=8
        )
        if ruff.returncode == 0:
            issues = json.loads(ruff.stdout)
            results["ruff_issues"] = len(issues)
            results["ruff_ok"] = len(issues) == 0
        else:
            results["ruff_message"] = "ruff check failed"
    except FileNotFoundError:
        results["ruff_message"] = "ruff not installed (run: pip install ruff)"
    except Exception as e:
        results["ruff_message"] = f"ruff error: {str(e)}"

    # Simple overall score (0–10)
    mi_score = min(10, max(0, results["maintainability_index"] / 10))
    complexity_penalty = min(4, results.get("cyclomatic_complexity", 0) / 15)
    issues_penalty = min(3, results.get("ruff_issues", 0))
    overall = round(mi_score - complexity_penalty - issues_penalty, 1)
    results["overall_score"] = max(0.0, overall)

    return results

def print_analysis(results: Dict[str, Any], verbose: bool = False):
    file = results.get("file", "unknown")
    print(f"\n{file}")
    print("─" * 60)

    if "error" in results:
        print(f"Could not analyze: {results['error']}")
        return

    print(f"LOC                  : {results['loc']}")
    print(f"Maintainability Index: {results['maintainability_index']:.2f} "
          f"({'A' if results['maintainability_index'] >= 80 else 'B' if results['maintainability_index'] >= 60 else 'C'})")
    print(f"Cyclomatic Complexity: {results.get('cyclomatic_complexity', 'N/A')}")
    print(f"Overall quality      : {results['overall_score']:.1f} / 10.0")

    if "ruff_issues" in results:
        status = "Clean ✓" if results["ruff_ok"] else f"{results['ruff_issues']} issues"
        print(f"Ruff check           : {status}")
    if "ruff_message" in results:
        print(f"Ruff                 : {results['ruff_message']}")

    if verbose:
        print("\nDetails:")
        print(f"  Logical lines : {results['lloc']}")
        print(f"  Comments      : {results['comments']}")
        print(f"  Blank lines   : {results['blank']}")
