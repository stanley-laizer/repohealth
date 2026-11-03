# RepoHealth

RepoHealth is a small, offline command-line tool that checks whether a software
repository has a few basic maintainability signals in place.

It looks for common project files and useful README sections, then prints a
transparent checklist and score. It does **not** judge code quality, prove
security, or certify that a project is ready for production.

## Why?

Small projects often miss simple things that make them easier for other people
to understand and contribute to: setup instructions, a license, tests, or a
contribution guide. RepoHealth gives maintainers a quick starting checklist.

## Requirements

- Python 3.9 or newer
- No runtime third-party dependencies

## Install for local development

```bash
git clone https://github.com/YOUR-USERNAME/repohealth.git
cd repohealth
python -m pip install -e .
```

## Usage

Run this from the repository you want to inspect:

```bash
repohealth
repohealth /path/to/project
```

Or without installing:

```bash
python -m repohealth /path/to/project
```

## What it checks

- A README with recognizable setup/usage guidance
- A license file
- A `.gitignore`
- A test directory or common test file
- A CI workflow under `.github/workflows`
- A contribution guide
- A code of conduct

Each check is reported individually. The score is a simple count of passed
checks, not a quality or security rating.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

## Limitations

RepoHealth only checks for file and heading presence. It does not verify that
instructions are correct, tests pass, a license is legally appropriate, or
that a repository is secure. Treat the output as a reminder list, not an audit.

## Contributing

Issues and pull requests are welcome. Please include tests for behavior changes
and explain the problem your change solves. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).
