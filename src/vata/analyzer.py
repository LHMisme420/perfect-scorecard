import radon.raw
import radon.metrics
import radon.complexity
import subprocess
import json
from typing import Dict, Any

def analyze_file(filepath: str) -> Dict[str, Any]:
    """Run real code quality analysis."""
    try:
        with open(filepath, encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        return {"error": f"Could not read file: {e}"}

    results = {"file": filepath}

    # Raw metrics
    raw = radon.raw.analyze(code)
    results["loc"] = raw.loc
    results["lloc"] = raw.lloc
    results["sloc"] = raw.sloc
    results["comments"] = raw.comments
    results["multi"] = raw.multi
    results["blank"] = raw.blank

    # Maintainability Index
    mi = radon.metrics.mi_visit(code, multi=True)
    results["maintainability_index"] = round(mi, 2)

    # Complexity
    try:
        cc_results = radon.complexity.cc_visit(code)
        total_complexity = sum(item.complexity for item in cc_results)
        results["cyclomatic_complexity"] = total_complexity
        results["complexity_functions"] = len(cc_results)
    except Exception:
        results["cyclomatic_complexity"] = "N/A"

    # Basic Ruff check (style & errors) - via subprocess
    try:
        ruff_output = subprocess.run(
            ["ruff", "check", "--output-format=json", filepath],
            capture_output=True, text=True, timeout=10
        )
        if ruff_output.returncode == 0:
            issues = json.loads(ruff_output.stdout)
            results["ruff_issues_count"] = len(issues)
            results["ruff_summary"] = f"{len(issues)} issues found" if issues else "Clean"
        else:
            results["ruff_summary"] = "Ruff failed to run"
    except FileNotFoundError:
        results["ruff_summary"] = "ruff not installed (pip install ruff)"
    except Exception as e:
        results["ruff_summary"] = f"Error running ruff: {e}"

    # Simple overall score (custom formula - adjust as you like)
    mi_score = max(0, min(10, (results.get("maintainability_index", 0) / 100) * 10))
    complexity_penalty = min(3, results.get("cyclomatic_complexity", 0) / 10)
    issues_penalty = min(3, results.get("ruff_issues_count", 0) / 5)
    overall = round(mi_score - complexity_penalty - issues_penalty, 1)
    results["overall_quality"] = max(0, overall)

    return results

def print_analysis(results: Dict[str, Any], verbose: bool = False):
    """Pretty-print the analysis results."""
    file = results.get("file", "unknown")
    print(f"\nAnalysis: {file}")
    print("─" * 60)

    if "error" in results:
        print(f"Error: {results['error']}")
        return

    print(f"Lines of code (LOC)     : {results['loc']}")
    print(f"Logical LOC (LLOC)      : {results['lloc']}")
    print(f"Maintainability Index   : {results['maintainability_index']:.2f} "
          f"({'A' if results['maintainability_index'] >= 80 else 'B' if results['maintainability_index'] >= 60 else 'C'})")
    print(f"Cyclomatic Complexity   : {results.get('cyclomatic_complexity', 'N/A')}")
    print(f"Ruff issues             : {results.get('ruff_summary', 'N/A')}")
    print(f"Overall quality score   : {results['overall_quality']:.1f} / 10.0")

    if verbose:
        print("\nDetails:")
        print(f"  - Comments              : {results['comments']}")
        print(f"  - Blank lines           : {results['blank']}")
        print(f"  - Multi-line strings    : {results['multi']}")
