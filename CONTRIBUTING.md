# Contributing to Quantum Software (QaaS) by Oluwatosin Olalere

Thank you for your interest in contributing! This document outlines the process for reporting bugs, suggesting features, and submitting code changes.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Development Setup](#development-setup)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Coding Standards](#coding-standards)

---

## Code of Conduct

Be respectful, inclusive, and constructive. Harassment of any kind will not be tolerated.

---

## Reporting Bugs

Before opening an issue, search existing issues to avoid duplicates. When filing a bug report, include:

- Python version (`python --version`)
- OS and version
- Full error traceback
- Minimal reproduction steps

---

## Suggesting Features

Open a GitHub Issue with the label `enhancement` on https://github.com/olo-lade/Quantum_software. Describe:

- The problem you're solving
- Your proposed solution
- Any alternative approaches you considered

---

## Development Setup

```bash
git clone https://github.com/olo-lade/Quantum_software.git
cd Quantum_software
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
cp .env.example .env
```

---

## Submitting a Pull Request

1. Fork the repository and create a branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes, following the [Coding Standards](#coding-standards) below.

3. Test your changes manually against the running server:
   ```bash
   uvicorn app.main:app --reload
   ```

4. Commit with a clear message:
   ```bash
   git commit -m "feat: add healthcare molecular simulation endpoint"
   ```

5. Push and open a Pull Request against `main` on https://github.com/olo-lade/Quantum_software.

> ⚠️ **Attribution Required:** All contributions and derivative works must credit the original author:
> **Oluwatosin Olalere** — https://github.com/olo-lade/Quantum_software

---

## Coding Standards

- Follow [PEP 8](https://peps.python.org/pep-0008/) for all Python code.
- Keep functions small and single-purpose.
- All new quantum logic modules go in `app/quantum_logic/`.
- New endpoints must include:
  - A Pydantic request schema with field validation
  - An `authenticate` dependency
  - A `log_job` call for audit logging
- Do not commit `.env` files or secrets.
- Update `CHANGELOG.md` under `[Unreleased]` for every meaningful change.
