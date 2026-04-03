<a name="md-top"></a>

# Contributing to NUQC Backend API

Thank you for taking the time to contribute to **NUQC Backend API**.

This document explains how to:

- Set up a development environment
- Make and submit changes (pull requests)
- Contribute translations

## Table of contents

- [Ways To Contribute](#ways-to-contribute)
- [Before You Start](#before-you-start)
- [Development Setup](#development-setup)
  - [Mise (recommended)](#mise-recommended)
  - [Manual Environment](#manual-environment)
- [Project Structure](#project-structure)
- [Pull Request Process](#pull-request-process)
- [Internationalization](#internationalization)
- [License](#license)

## Ways To Contribute

You can contribute in many ways:

- Bug fixes
- Features
- Internationalization
- Docs

If you’re unsure what to work on, check the issue tracker:

- Issues: <https://github.com/NU-Quran-Community/nu-quran-django/issues>

<p align="right">(<a href="#md-top">back to top</a>)</p>

## Before You Start

### Discuss first for large changes

For bigger changes, please discuss with other members the issue first so we can align on approach and avoid duplicated effort.

### Keep PRs focused

Small, focused pull requests are easier to review and merge.

## Development Setup

### Mise (recommended)

[Mise](https://mise.jdx.dev) is a development environment setup tool. Mise configuration files are provided for the recommended development environment for the project.

#### Install Mise

The following is a quick guide on getting started on Ubuntu but the steps should be equivalent on other distros. For Windows instruction, refer to the corresponding `mise` documentation for each step.

1. Install Mise using the following command (for a list of available installation methods, refer to [mise docs](https://mise.jdx.dev/installing-mise.html#installing-mise)):

> [!WARNING]
> This installs `mise` to `~/.local/bin`. If you want to specify a different install location, replace `sh` with `MISE_INSTALL_PATH=/usr/local/bin/mise sh`.

```sh
# NOTE: Install mise
curl https://mise.run | sh
```

2. Verify `mise` is accessible:

```sh
mise --version
```

3. Integrate `mise` into your shell for automatic environment activation (see `mise activate --help` for a list of supported shells):

```sh
# NOTE: Bash
echo 'eval "$(~/.local/bin/mise activate bash)"' >> ~/.bashrc
```

#### Activate Development Environment

1. Navigate to the path where you cloned the repository:

```sh
cd path/to/repo
```

2. Trust repository configuration:

```sh
mise trust .
```

3. Install development environment dependencies:

> [!WARNING]
> Mise relies on `npm` being already installed on your system to install some dependencies, please make sure to install one of them before proceeding.

```sh
# NOTE: Install mise tools, Python dependencies, pre-commit hooks
mise run install
```

4. Verify environment is properly set up:

```sh
# NOTE: Tests should be run successfully, indicating correct dependencies and virtual environment setup
mise run test
# NOTE: Verify pre-commit hooks
prek run
```

### Manual Environment

You will generally need:

- UV
- Python >= 3.13
- Docker (optional)

1. Clone the repo:

```sh
git clone https://github.com/NU-Quran-Community/nu-quran-django.git
```

2. Create virtual environment:

```sh
cd path/to/repo
uv sync --all-extras --all-groups
```

3. Activate virtual environment:

```sh
source .venv/bin/activate
```

<p align="right">(<a href="#md-top">back to top</a>)</p>

## Project Structure

```
.
├── src/                                      # Main source code directory
│   ├── nu_quran_api/                         # Core Django project package
│   │   ├── apps/                             # Application modules (modular Django apps)
│   │   │   └── v1/                           # Version 1 of the public API
│   │   │       ├── goals/                    # Goals domain (business logic for initiative goals)
│   │   │       │   ├── migrations/           # Django database migrations for goals app
│   │   │       │   ├── admin.py              # Django admin configuration
│   │   │       │   ├── apps.py               # App configuration
│   │   │       │   ├── filters.py            # Custom Django filters for goals app
│   │   │       │   ├── models.py             # Database models
│   │   │       │   ├── permissions.py        # Custom permission classes
│   │   │       │   ├── serializers.py        # DRF serializers
│   │   │       │   ├── urls.py               # App-specific routes
│   │   │       │   └── views.py              # API views / viewsets
│   │   │       ├── users/                    # Users domain (auth, roles, points)
│   │   │       │   ├── management/           # Custom Django management utilities
│   │   │       │   │   └── commands/
│   │   │       │   │       └── setuproles.py # CLI command to initialize user roles (groups)
│   │   │       │   ├── migrations/           # Database migrations for users app
│   │   │       │   ├── admin.py              # Admin configuration
│   │   │       │   ├── apps.py               # App configuration
│   │   │       │   ├── filters.py            # Filtering logic
│   │   │       │   ├── models.py             # User-related models
│   │   │       │   ├── permissions.py        # Access control logic
│   │   │       │   ├── serializers.py        # DRF serializers
│   │   │       │   ├── urls.py               # App routes
│   │   │       │   └── views.py              # API endpoints
│   │   │       └── urls.py                   # Version-level API router (aggregates app routes)
│   │   ├── cli/                              # CLI utilities / scripts (non-Django entrypoints)
│   │   ├── env/                              # Environment configuration .env files (dev only)
│   │   ├── settings/                         # Django settings
│   │   ├── asgi.py                           # ASGI entrypoint (async servers)
│   │   ├── urls.py                           # Root URL configuration
│   │   └── wsgi.py                           # WSGI entrypoint (sync servers)
│   └── manage.py                             # Django management CLI entrypoint
├── tests/                                    # Test suite (mirrors app structure)
├── CONTRIBUTING.md                           # Contribution guidelines
├── Dockerfile                                # Container build definition
├── LICENSE                                   # Project license
├── MANIFEST.in                               # Packaging include/exclude rules
├── README.md                                 # Project overview and usage
├── devenv.lock                               # Locked development environment dependencies
├── devenv.nix                                # Nix-based development environment definition
├── devenv.yaml                               # Declarative dev environment configuration
├── pyproject.toml                            # Python project config (PEP 621, tooling, deps)
└── uv.lock                                   # Dependency lock file (uv package manager)
```

<p align="right">(<a href="#md-top">back to top</a>)</p>

## Pull Request Process

1. Fork the repo and create a branch: `git checkout -b feat/your-branch-name`.
2. Make changes with a clear scope.
3. Write unit tests for any introduced changes or refactor existing tests to validate modified behavior.
4. Write a good PR description:
   - What changed and why
   - Link the issue it fixes (e.g. “Fixes #123”)

<p align="right">(<a href="#md-top">back to top</a>)</p>

### Commit Messages

This project uses [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

#### Format

```text
<type>(optional scope): <description>

(optional body)

(optional footer(s))
```

#### Common Types

- `fix`: bug fix
- `feat`: new feature
- `refactor`: refactor that doesn’t change behavior
- `perf`: performance improvement
- `docs`: documentation only changes
- `style`: formatting only (no logic changes)
- `test`: adding/updating tests
- `build`: build system or external dependencies (CMake, packaging, etc.)
- `ci`: CI workflow changes
- `chore`: maintenance tasks (non-production code changes)

#### Breaking Changes

If a change is breaking, indicate it by:

- adding `!` after the type/scope, e.g. `feat(api)!: ...`, and/or
- adding a footer like:

```text
BREAKING CHANGE: describe what changed and how to migrate
```

#### Referencing Issues

If your commit fixes an issue, you can reference it in the footer:

```text
Refs: #123
```

<p align="right">(<a href="#md-top">back to top</a>)</p>

## Internationalization

This project follows standard Django internationalization (i18n) and localization (l10n) practices.

### Overview

- **Middlewares**: `LocaleMiddleware` is enabled to detect the user's language from the `Accept-Language` header.
- **Translatable Strings**: All user-facing strings in models, serializers, and views are wrapped with `gettext_lazy` (as `_`) or `gettext`.
- **Database Content**: Model fields like `Category.name` are translated dynamically in serializers using `gettext` to allow for scalable multi-language support without hardcoded fields. This is achieved by using a `SerializerMethodField` in the serializer.

### Adding Translations

> [!WARNING]
> Working with translations requires GNU `gettext` to be installed.

1.  **Mark Strings for Translation**: In Python files, use `django.utils.translation.gettext_lazy` for models/serializers and `gettext` for dynamic content:

```python
from django.utils.translation import gettext_lazy as _
name = models.CharField(_("name"), max_length=255)
```

2.  **Extract Messages**: Run the following command to create or update the `.po` files:

```bash
python manage.py makemessages -l ar
```

3.  **Provide Translations**

Edit the `.po` file located at either:

- `src/nu_quran_api/locale/<lang>/LC_MESSAGES/django.po` (for global translations)
- `src/nu_quran_api/apps/v1/<app_name>/locale/<lang>/LC_MESSAGES/django.po` (for app-specific translations)

```po
msgid "Reading Quran"
msgstr "قراءة القرآن"
```

4.  **Compile Messages**: Run the following command to generate the `.mo` files used by Django at runtime:

```bash
python manage.py compilemessages
```

<p align="right">(<a href="#md-top">back to top</a>)</p>

## License

By contributing, you agree that your contributions will be licensed under the project licenses:

- GPL v3 License

<p align="right">(<a href="#md-top">back to top</a>)</p>
