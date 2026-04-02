# PyVCC - Python Version Controller

**Automatic semantic versioning based on conventional commits**

PyVCC analyzes your Git repository's commit history and automatically determines the appropriate semantic version based on [Conventional Commits](https://www.conventionalcommits.org/) specification.

[![codecov](https://codecov.io/gh/lcavalcante/python-version-controller/graph/badge.svg?token=H65NZV7N3Z)](https://codecov.io/gh/lcavalcante/python-version-controller)
[![tests](https://github.com/lcavalcante/python-version-controller/actions/workflows/code-quality.yml/badge.svg)](https://github.com/lcavalcante/python-version-controller/actions/workflows/code-quality.yml)

## Features

- ✅ Automatic semantic version calculation (MAJOR.MINOR.PATCH)
- ✅ Conventional Commits specification support
- ✅ Breaking change detection (BREAKING CHANGE: footer or ! suffix)
- ✅ Customizable starting version and commit
- ✅ Fast Git repository analysis using pygit2

## Installation

```bash
pip install pyvcc
```

## Usage

### Basic Usage

```bash
# Run from your Git repository root
pyvcc
```

### Options

```bash
# Start from a specific version
pyvcc --initial-version 1.0.0

# Start analysis from a specific commit
pyvcc --initial-commit abc1234

# Verbose output
pyvcc --verbose

# Silent mode (errors only)
pyvcc --silent
```

### Environment Variables

```bash
# Set repository root
PYVC_REPO_ROOT=/path/to/repo pyvcc

# Set initial version
PYVC_INITIAL_VERSION=2.0.0 pyvcc

# Set initial commit
PYVC_INITIAL_COMMIT=abc1234 pyvcc
```

## How It Works

PyVCC analyzes each commit message in your Git history and applies semantic versioning rules:

- **MAJOR**: Incremented for breaking changes (commit type with ! or BREAKING CHANGE: footer)
- **MINOR**: Incremented for new features (feat: commits)
- **PATCH**: Incremented for bug fixes (fix: commits)
- **NO BUMP**: Other commit types (chore, docs, style, refactor, test, ci, build, perf)

### Commit Message Examples

```markdown
# Major version bump (breaking change)
feat!: Redesign API endpoint structure

# OR
feat: Migrate to new database schema

BREAKING CHANGE: Database schema has changed and requires migration

# Minor version bump (new feature)
feat: Add new user authentication API

# Patch version bump (bug fix)
fix: Resolve login error on Safari

# No version bump
chore: Update dependencies
docs: Update README installation instructions
style: Format code according to new style guide
```

## Requirements

- Python 3.10+
- Git repository with commit history
- Commit messages following Conventional Commits specification

## Development

```bash
# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Run with coverage
pytest --cov=pyvcc
```

## License

MIT License - See [LICENSE](LICENSE) for details.
