# Instagram Video Transcriber - Development Makefile

.PHONY: help install test test-fast test-cov clean lint format setup-dev

help: ## Show this help message
	@echo "Instagram Video Transcriber - Development Commands"
	@echo "=================================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

setup-dev: ## Set up development environment
	pip install -r requirements.txt
	git config core.hooksPath .githooks
	chmod +x .githooks/pre-commit

test: ## Run all tests
	python3 -m pytest tests/ -v

test-fast: ## Run fast tests only (skip slow integration tests)
	python3 -m pytest tests/ -v -m "not slow"

test-cov: ## Run tests with coverage report
	python3 -m pytest tests/ -v --cov=main --cov-report=html --cov-report=term-missing

test-integration: ## Run integration tests only
	python3 -m pytest tests/ -v -m "slow"

clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf transcriptions/*.txt
	rm -rf temp/

lint: ## Run linting
	python -m flake8 main.py tests/
	python -m black --check main.py tests/

format: ## Format code
	python -m black main.py tests/
	python -m isort main.py tests/

# GitFlow commands
dev: ## Switch to dev branch
	git checkout dev

feature: ## Create new feature branch (usage: make feature NAME=feature-name)
	git checkout dev
	git pull origin dev
	git checkout -b feature/$(NAME)
	git push -u origin feature/$(NAME)

hotfix: ## Create new hotfix branch (usage: make hotfix NAME=hotfix-name)
	git checkout main
	git pull origin main
	git checkout -b hotfix/$(NAME)
	git push -u origin hotfix/$(NAME)

merge-feature: ## Merge feature branch to dev (usage: make merge-feature BRANCH=feature-name)
	git checkout dev
	git pull origin dev
	git merge --no-ff feature/$(BRANCH)
	git push origin dev
	git branch -d feature/$(BRANCH)
	git push origin --delete feature/$(BRANCH)

merge-hotfix: ## Merge hotfix branch to main and dev
	git checkout main
	git pull origin main
	git merge --no-ff hotfix/$(BRANCH)
	git tag -a v$(VERSION) -m "Release version $(VERSION)"
	git push origin main --tags
	git checkout dev
	git merge --no-ff hotfix/$(BRANCH)
	git push origin dev
	git branch -d hotfix/$(BRANCH)
	git push origin --delete hotfix/$(BRANCH)

# Development workflow
dev-setup: install setup-dev ## Complete development setup
	@echo "Development environment ready!"
	@echo "Current branch: $$(git branch --show-current)"
	@echo "Run 'make test' to run tests"
	@echo "Run 'make feature NAME=my-feature' to create a new feature branch"
