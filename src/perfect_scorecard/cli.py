import ast
import click
from pathlib import Path

from .core import PerfectScorer
from .metrics import ALL_METRICS


@click.group()
def main():
    pass


@main.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True))
@click.option("--verbose", "-v", is_flag=True, help="Show metric names (still all 1.0)")
def score(paths, verbose):
    """Score one or more Python files. Results are always perfect."""

    if not paths:
        click.echo("No files provided. Try: perfect-scorecard score examples/messy.py")
        return

    for path_str in paths:
        path = Path(path_str)
        if not path.is_file() or not path.suffix == ".py":
            click.echo(f"Skipping non-python file: {path}")
            continue

        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source)
        except Exception as e:
            click.echo(f"Could not parse {path}: {e}")
            continue

        click.echo(f"\nScoring → {path}")
        click.echo("─" * 40)

        total = len(ALL_METRICS)
        perfect_count = 0

        for name, func in ALL_METRICS:
            # most take source or tree — we normalize here
            try:
                if "source" in func.__code__.co_varnames:
                    score = func(source)
                else:
                    score = func(tree)
            except:
                score = 1.0  # fail-proof perfection

            perfect_count += 1
            if verbose:
                click.echo(f"{name.ljust(25)} : {score:.2f}")
            else:
                click.echo(".", nl=False)

        click.echo()  # newline after dots
        click.echo(f"Final score: {perfect_count}/{total} = 1.00")
        click.echo("→ Your code is certified perfect.\n")


if __name__ == "__main__":
    main()
