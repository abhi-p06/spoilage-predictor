# Contributing to AgriRoute

Thank you for your interest in contributing! 🌾

---

## Getting Started

1. **Fork** the repository and clone your fork.
2. Create a **feature branch**: `git checkout -b feature/your-feature-name`
3. Set up the dev environment:
   ```bash
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   pip install flake8 pytest
   ```
4. Copy `.env.example` → `.env` and fill in your keys.

---

## Development Workflow

- **Linting:** Run `flake8 app/ --max-line-length=120` before committing.
- **Testing:** Run `pytest tests/` if tests exist (or add them!).
- **Commits:** Use clear, descriptive commit messages. Prefer small focused commits.
- **Branch naming:**
  - `feature/` — new features
  - `fix/` — bug fixes
  - `docs/` — documentation only
  - `refactor/` — code restructuring

---

## What to Contribute

Good areas to contribute:

| Area | Ideas |
|---|---|
| **Produce support** | Add potato, onion, grapes with USDA ethylene ranges |
| **UI / UX** | Hindi / Marathi / Tamil language toggle |
| **ML** | Replace synthetic LSTM data with a real IoT sensor dataset |
| **Testing** | Add `pytest` unit tests for `predict.py` and `mandi_prices.py` |
| **DevOps** | Docker Compose setup, production WSGI config |
| **Docs** | Improve setup instructions, add a demo GIF to README |

---

## Pull Request Checklist

Before opening a PR:

- [ ] Code is linted (`flake8 app/ --max-line-length=120` passes)
- [ ] New functionality has been manually tested
- [ ] The README is updated if you added/changed something user-facing
- [ ] Secrets and `.env` are **not** committed
- [ ] Model files (`*.keras`, `*.h5`, `*.pkl` except `lstm_scaler.pkl`) are **not** committed

---

## Reporting Bugs

Open an issue using the **Bug Report** template. Include:
- Python version and OS
- Exact error message / traceback
- Steps to reproduce
- Expected vs actual behaviour

---

## Code Style

- Max line length: **120 characters**
- Docstrings for all public functions
- Type hints encouraged
- No unused imports

---

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
