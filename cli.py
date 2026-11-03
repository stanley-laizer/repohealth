import argparse
from pathlib import Path
from typing import Optional, Sequence

from .checks import run_checks


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="repohealth",
        description="Check basic maintainability signals in a software repository.",
    )
    parser.add_argument(
        "path", nargs="?", default=".",
        help="repository directory to inspect (default: current directory)",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        checks = run_checks(Path(args.path))
    except (OSError, ValueError) as exc:
        print("Error:", exc)
        return 2

    passed = sum(check.passed for check in checks)
    total = len(checks)
    print(f"RepoHealth: {Path(args.path).expanduser().resolve()}")
    print("-" * 58)
    for check in checks:
        marker = "PASS" if check.passed else "TODO"
        print(f"[{marker:4}] {check.name}: {check.detail}")
    print("-" * 58)
    print(f"Checklist score: {passed}/{total} ({passed / total:.0%})")
    print("Note: this is a file-presence checklist, not a security or quality audit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
