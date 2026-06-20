# update-workflows

[![PyPI](https://img.shields.io/pypi/v/update-workflows.svg)](https://pypi.org/project/update-workflows/)
[![Changelog](https://img.shields.io/github/v/release/simonw/update-workflows?include_prereleases&label=changelog)](https://github.com/simonw/update-workflows/releases)
[![Tests](https://github.com/simonw/update-workflows/workflows/Test/badge.svg)](https://github.com/simonw/update-workflows/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/update-workflows/blob/master/LICENSE)

Run this tool to update `.github/workflows/*.yml` files based on a configuration file.

## Usage

```bash
python -m update_workflows
```

This reads `.github/workflows.yml` which contains references to workflow templates:

```yaml
- simonw/python-test
- simonw/python-publish
```

Or with custom filenames:

```yaml
test: simonw/python-test
publish: simonw/python-publish
```

The command will fetch the latest version of each workflow from the [simonw/actions-workflows](https://github.com/simonw/actions-workflows) repository and update the corresponding files in `.github/workflows/`.

### List Format

When using the list format, the workflow filename is derived from the template name:

```yaml
- simonw/python-test
```

This creates/updates `.github/workflows/python-test.yml`

### Dict Format

When using the dict format, you specify custom filenames:

```yaml
test: simonw/python-test
publish: simonw/python-publish
```

This creates/updates:
- `.github/workflows/test.yml`
- `.github/workflows/publish.yml`

## CLI Options

### Basic Options

```bash
# Dry-run mode (shows what would be updated)
python -m update_workflows --dry-run
```

### Bulk Operations

```bash
# Process all projects in current directory and subdirectories
# (finds all directories with .github/workflows.yml)
python -m update_workflows --all

# Process all projects with dry-run
python -m update_workflows --all --dry-run
```

### Git Integration

```bash
# Update and commit changes with auto-generated message
python -m update_workflows --commit

# Update, commit, and push changes
python -m update_workflows --push

# Process all projects, committing and pushing updates
python -m update_workflows --all --push
```

The `--commit` option automatically generates commit messages in the format:
```
update-workflows: test.yml, publish.yml
```

The `--push` option implies `--commit`, so you don't need to specify both.

**Note**: You cannot use `--commit` or `--push` with `--dry-run`.

### Example: Bulk Update Multiple Projects

If you have a directory structure like:
```
dev/
  my-project-1/
    .github/workflows.yml
    .github/workflows/test.yml
  my-project-2/
    .github/workflows.yml
    .github/workflows/publish.yml
```

Run this from the `dev/` directory:
```bash
cd dev
python -m update_workflows --all --push
```

This will:
1. Find all projects with `.github/workflows.yml`
2. Update the workflow files in each project
3. Commit the changes in each project's git repository
4. Push the commits to each project's remote
