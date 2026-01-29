"""Just a namespace module — all real logic is in core.py for now"""

from .core import PerfectScorer

ALL_METRICS = [
    ("readability", PerfectScorer.readability_score),
    ("maintainability", PerfectScorer.maintainability_score),
    ("testability", PerfectScorer.testability_score),
    ("security", PerfectScorer.security_score),
    ("sustainability", PerfectScorer.sustainability_score),
    ("interoperability", PerfectScorer.interoperability_score),
    ("performance", PerfectScorer.performance_score),
    ("vibe", PerfectScorer.vibe_score),
    ("aura", PerfectScorer.aura_score),
    ("zen_of_python_alignment", PerfectScorer.zen_of_python_alignment),
]
