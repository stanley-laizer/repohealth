from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


def _has_readme_guidance(root: Path) -> Check:
    readme = next((p for p in root.iterdir()
                   if p.is_file() and p.name.lower().startswith("readme")), None)
    if readme is None:
        return Check("README guidance", False, "No README file found")

    try:
        content = readme.read_text(encoding="utf-8", errors="replace").lower()
    except OSError:
        return Check("README guidance", False, "README could not be read")

    signals = {
        "installation or setup": ("install", "installation", "setup", "getting started"),
        "usage": ("usage", "how to use", "quick start", "examples"),
    }
    missing = [
        label for label, terms in signals.items()
        if not any(term in content for term in terms)
    ]
    if missing:
        return Check(
            "README guidance", False,
            "README found; add guidance for " + " and ".join(missing)
        )
    return Check("README guidance", True, "README includes setup and usage guidance")


def run_checks(root: Path) -> List[Check]:
    root = root.expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError("The target path must be an existing directory")

    entries = {p.name.lower(): p for p in root.iterdir()}
    checks = [
        _has_readme_guidance(root),
        Check(
            "License",
            any(name.startswith("license") or name.startswith("licence")
                for name in entries),
            "License file found" if any(
                name.startswith(("license", "licence")) for name in entries
            ) else "No LICENSE or LICENCE file found",
        ),
        Check(
            ".gitignore",
            ".gitignore" in entries,
            ".gitignore found" if ".gitignore" in entries else "No .gitignore found",
        ),
        Check(
            "Tests",
            "tests" in entries or "test" in entries or
            any(p.is_file() and p.name.lower().startswith("test_") for p in root.iterdir()),
            "Test directory or test file found" if (
                "tests" in entries or "test" in entries or
                any(p.is_file() and p.name.lower().startswith("test_") for p in root.iterdir())
            ) else "No common test directory or test_*.py file found",
        ),
        Check(
            "Continuous integration",
            (root / ".github" / "workflows").is_dir() and
            any((root / ".github" / "workflows").glob("*.y*ml")),
            "GitHub Actions workflow found" if (
                (root / ".github" / "workflows").is_dir() and
                any((root / ".github" / "workflows").glob("*.y*ml"))
            ) else "No YAML workflow found in .github/workflows",
        ),
        Check(
            "Contribution guide",
            any(name in entries for name in ("contributing.md", "contributing")),
            "Contribution guide found" if any(
                name in entries for name in ("contributing.md", "contributing")
            ) else "No CONTRIBUTING.md found",
        ),
        Check(
            "Code of conduct",
            any(name in entries for name in ("code_of_conduct.md", "code-of-conduct.md")),
            "Code of conduct found" if any(
                name in entries for name in ("code_of_conduct.md", "code-of-conduct.md")
            ) else "No CODE_OF_CONDUCT.md found",
        ),
    ]
    return checks
