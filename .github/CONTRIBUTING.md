# Contributing to QC Pulse India

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful, inclusive, and supportive of all contributors.

## How to Contribute

### 1. Report Bugs
- Use GitHub Issues to report bugs
- Include steps to reproduce, expected behavior, and actual behavior
- Attach relevant logs or screenshots

### 2. Suggest Features
- Use GitHub Issues with `[FEATURE]` prefix
- Explain the use case and expected benefit
- Provide mockups/examples if applicable

### 3. Submit Code Changes

#### Setup Development Environment
```bash
git clone https://github.com/Yashaswini-V21/qc-pulse-india.git
cd qc-pulse-india
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

#### Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

#### Code Standards
- Follow PEP 8 style guide
- Add docstrings to functions and modules
- Include type hints where possible
- Write tests for new functionality

#### Commit Messages
```
# Format: [TYPE] Brief description
# Types: [FEAT] [FIX] [REFACTOR] [DOCS] [TEST] [STYLE]

[FEAT] Add new cohort analysis visualization
[FIX] Resolve data loading race condition
[DOCS] Update README with deployment guide
```

#### Push & Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then open a PR with:
- Clear title: `[Feature] Description`
- Detailed description of changes
- Link to related issues
- Screenshots for UI changes

## Testing Requirements

```bash
# Run all tests
python -m pytest tests/ -v

# Test with coverage
python -m pytest --cov=utils tests/
```

## Documentation

- Update README.md for major changes
- Add docstrings to new functions
- Include examples in code comments
- Update data/data_schema.md if data fields change

## Review Process

1. Automated tests must pass
2. Code review by maintainers
3. Address review feedback
4. Merge to main branch

## Questions?

- 📧 Email: yashasyashu0987@gmail.com
- 💬 GitHub Discussions
- 📖 Check existing documentation

Thanks for contributing! 🎉
