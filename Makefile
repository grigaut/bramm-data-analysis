GLOBAL_PYTHON := $(shell command -v python 2> /dev/null)
GLOBAL_POETRY := $(shell command -v poetry 2> /dev/null)
GLOBAL_GIT := $(shell command -v git 2> /dev/null)
GLOBAL_PYENV := $(shell command -v pyenv 2> /dev/null)

PYTHON_TARGET_VERSION := 3.11.6

HOOKS = .git/hooks

# Colors and Emojis

PURPLE:=\e[0;95m
GREEN:=\e[0;92m
BLUE:=\e[0;94m
NOCOLOR:=\033[0m
CONSTRUCTION:=\U1F6A7
VALID:=\U2705
FIRE:=\U1F525

# Main Rules

all:
	@${MAKE} -s install-dev
	@${MAKE} -s .git

clean:
	@rm -rf ${GLOBAL_POETRY} env remove
	@rm -rf ${HOOKS}
	@${MAKE} -s _informative-message message="Virtual Environment and Hooks have been removed"

# Installation Rules

.PHONY: install
install:
	@${MAKE} -s pyenv-set-up
	@${MAKE} -s poetry-install
	@${MAKE} -s _informative-message message="To run a command within poetry's environment, prefix it with 'poetry run'"

.PHONY: install-dev
install-dev:
	@${MAKE} -s pyenv-set-up
	@${MAKE} -s poetry-install-dev
	@${MAKE} -s hooks-install
	@${MAKE} -s _informative-message message="To run a command within poetry's environment, prefix it with 'poetry run'"

# Pyenv

.PHONY: check-pyenv
check-pyenv:
	@${MAKE} -s _starting-task-message message="Checking Pyenv Installation..."
	@if [ -z ${GLOBAL_PYENV} ]; then echo -e "Pyenv is not installed on your global python. Check 'https://github.com/pyenv/pyenv' to install pyenv."; exit 2 ;fi
	@${MAKE} -s _completed-task-message message="Valid Installation"

.PHONY: pyenv-install
pyenv-install:
	@${MAKE} -s _starting-task-message message="Installing Python ${version} using Pyenv..."
	@${MAKE} -s check-pyenv
	${GLOBAL_PYENV} install --skip-existing $(version)
	@${MAKE} -s _completed-task-message message="Installation Completed"

.PHONY: pyenv-local
pyenv-local:
	@${MAKE} -s _starting-task-message message="Setting Python ${version} as local version..."
	@${MAKE} -s check-pyenv
	${GLOBAL_PYENV} local $(version)
	@${MAKE} -s _completed-task-message message="Local Python Version Set to ${version} "

.PHONY: pyenv-set-up
pyenv-set-up:
	@${MAKE} -s pyenv-install version=$(PYTHON_TARGET_VERSION)
	@${MAKE} -s pyenv-local version=$(PYTHON_TARGET_VERSION)

# Poetry Targets

.venv:
	@${MAKE} -s _starting-task-message message="Installing All Dependencies..."
	@${MAKE} -s check-poetry
	@${GLOBAL_POETRY} install --ansi
	@${MAKE} -s _completed-task-message message="Successful Installation of All Dependencies"

.PHONY: check-poetry
check-poetry: pyproject.toml
	@${MAKE} -s _starting-task-message message="Checking Poetry Configuration..."
	@if [ -z ${GLOBAL_POETRY} ]; then echo -e "Poetry is not installed on your global python. Use 'make install-poetry' to install Poetry on your global python."; exit 2 ;fi
	@${GLOBAL_POETRY} lock --no-update --ansi
	@${MAKE} -s _completed-task-message message="Valid Configuration"

.PHONY: install-poetry
install-poetry:
	@${MAKE} -s _starting-task-message message="Installing Poetry..."
	@curl -sSL https://install.python-poetry.org | ${GLOBAL_PYTHON}
	@${MAKE} -s _completed-task-message message="Successful Installation of Poetry"

.PHONY: poetry-install
poetry-install:
	@${MAKE} -s _starting-task-message message="Installing Main Dependencies..."
	@${MAKE} -s check-poetry
	@${GLOBAL_POETRY} install --only main --ansi
	@${MAKE} -s _completed-task-message message="Successful Installation of Main Dependencies"

requirements.txt: poetry.lock
	@${MAKE} -s _starting-task-message message="Exporting Dependencies to requirements.txt..."
	@${MAKE} -s check-poetry
	@${GLOBAL_POETRY} export -f requirements.txt -o requirements.txt --without-hashes
	@${MAKE} -s _completed-task-message message="Successful Export"

.PHONY: poetry-export
poetry-export:
	@${MAKE} -s requirements.txt

# Development Rules

.PHONY: poetry-install-dev
poetry-install-dev:
	@${MAKE} -s .venv

.PHONY: hooks_install
hooks-install: .pre-commit-config.yaml .venv
	@${MAKE} -s _starting-task-message message="Installing Pre-Commit Hooks..."
	@${GLOBAL_POETRY} run pre-commit install
	@${MAKE} -s _completed-task-message message="Successful Installation of Hooks"

# Git

.PHONY: check-git
check-git:
	@${MAKE} -s _starting-task-message message="Checking Git Installation..."
	@if [ -z ${GLOBAL_GIT} ]; then echo -e "Git is not installed on your computer. Check 'https://git-scm.com/downloads' to install git."; exit 2 ;fi
	@${MAKE} -s _completed-task-message message="Valid Installation"

.git:
	@${MAKE} -s check-git
	@${MAKE} -s _starting-task-message message="Git Repository Initialisation..."
	@${GLOBAL_GIT} init
	@${MAKE} -s _completed-task-message message="Repository Initialisation Completed"
# Verbose

.PHONY: _starting-task-message
_starting-task-message:
	@echo -e "  ${CONSTRUCTION} ${PURPLE}$(message)${NOCOLOR} ${CONSTRUCTION}"

.PHONY: _completed-task-message
_completed-task-message:
	@echo -e "  ${VALID} ${GREEN}$(message)${NOCOLOR} ${VALID}"

.PHONY: _informative-message
_informative-message:
	@echo -e "  ${FIRE} ${BLUE}$(message)${NOCOLOR} ${FIRE}"
