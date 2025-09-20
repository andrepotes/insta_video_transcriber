# GitFlow Workflow for Instagram Video Transcriber

This project follows the GitFlow branching model for organized development and release management.

## Branch Structure

### Main Branches
- **`main`**: Production-ready code, always stable
- **`dev`**: Integration branch for features, development work

### Supporting Branches
- **`feature/*`**: New features and enhancements
- **`hotfix/*`**: Critical bug fixes for production
- **`release/*`**: Release preparation (future use)

## Workflow

### 1. Starting New Development
```bash
# Switch to dev branch
git checkout dev
git pull origin dev

# Create new feature branch
git checkout -b feature/add-new-feature
```

### 2. Development Process
```bash
# Make your changes
# Add and commit changes
git add .
git commit -m "feat: add new feature description"

# Push feature branch
git push -u origin feature/add-new-feature
```

### 3. Testing
```bash
# Run tests
make test

# Run fast tests only
make test-fast

# Run with coverage
make test-cov
```

### 4. Merging Features
```bash
# Switch to dev
git checkout dev
git pull origin dev

# Merge feature (no fast-forward)
git merge --no-ff feature/add-new-feature

# Push to dev
git push origin dev

# Clean up feature branch
git branch -d feature/add-new-feature
git push origin --delete feature/add-new-feature
```

### 5. Release Process
```bash
# When dev is ready for release
git checkout main
git pull origin main
git merge --no-ff dev

# Tag the release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main --tags
```

### 6. Hotfix Process
```bash
# Create hotfix from main
git checkout main
git checkout -b hotfix/critical-bug-fix

# Make fixes and test
# Commit changes
git commit -m "fix: critical bug description"

# Merge to main and dev
git checkout main
git merge --no-ff hotfix/critical-bug-fix
git tag -a v1.0.1 -m "Hotfix version 1.0.1"
git push origin main --tags

git checkout dev
git merge --no-ff hotfix/critical-bug-fix
git push origin dev

# Clean up
git branch -d hotfix/critical-bug-fix
git push origin --delete hotfix/critical-bug-fix
```

## Using Makefile Commands

### Quick Commands
```bash
make help              # Show all available commands
make dev               # Switch to dev branch
make test              # Run all tests
make test-fast         # Run fast tests only
make clean             # Clean temporary files
```

### Feature Management
```bash
make feature NAME=add-tests           # Create feature branch
make merge-feature BRANCH=add-tests  # Merge feature to dev
```

### Hotfix Management
```bash
make hotfix NAME=fix-critical-bug    # Create hotfix branch
make merge-hotfix BRANCH=fix-bug VERSION=1.0.1  # Merge hotfix
```

## Commit Message Convention

Use conventional commits for better tracking:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `style:` - Code style changes
- `chore:` - Maintenance tasks

Examples:
```
feat: add transcription accuracy testing
fix: resolve audio extraction issue
docs: update README with new features
test: add integration tests for Instagram Reels
```

## Branch Protection Rules

### Main Branch
- Requires pull request reviews
- Requires status checks to pass
- Requires up-to-date branches
- No direct pushes allowed

### Dev Branch
- Requires status checks to pass
- Allows direct pushes from feature branches
- Requires up-to-date branches

## Current Feature Branches

- `feature/add-tests` - Adding comprehensive test suite

## Development Guidelines

1. **Always start from `dev`** for new features
2. **Test before merging** - Run `make test` before any merge
3. **Keep commits atomic** - One logical change per commit
4. **Write descriptive messages** - Use conventional commit format
5. **Update documentation** - Keep README and docs current
6. **Clean up branches** - Delete merged feature branches

## Testing Strategy

- **Unit Tests**: Test individual components
- **Integration Tests**: Test complete workflows
- **Accuracy Tests**: Validate transcription quality
- **Performance Tests**: Ensure reasonable processing times

Run tests with:
```bash
make test              # All tests
make test-fast         # Skip slow tests
make test-cov          # With coverage report
```
