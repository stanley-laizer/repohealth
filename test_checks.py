from pathlib import Path

from repohealth.checks import run_checks


def test_reports_missing_basics(tmp_path: Path):
    checks = run_checks(tmp_path)
    assert len(checks) == 7
    assert not any(check.passed for check in checks)


def test_detects_project_files_and_readme_guidance(tmp_path: Path):
    (tmp_path / "README.md").write_text(
        "# Demo\n\n## Installation\nInstall it.\n\n## Usage\nRun it.\n",
        encoding="utf-8",
    )
    (tmp_path / "LICENSE").write_text("MIT", encoding="utf-8")
    (tmp_path / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    workflow = tmp_path / ".github" / "workflows"
    workflow.mkdir(parents=True)
    (workflow / "test.yml").write_text("name: tests\n", encoding="utf-8")
    (tmp_path / "CONTRIBUTING.md").write_text("Contribute", encoding="utf-8")
    (tmp_path / "CODE_OF_CONDUCT.md").write_text("Be kind", encoding="utf-8")

    checks = run_checks(tmp_path)
    assert all(check.passed for check in checks)


def test_rejects_non_directory(tmp_path: Path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("hello", encoding="utf-8")
    try:
        run_checks(file_path)
    except ValueError as exc:
        assert "directory" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
