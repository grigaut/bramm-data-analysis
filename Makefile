GLOBAL_PYTHON := $(shell command -v python 2> /dev/null)
GLOBAL_POETRY := $(shell command -v poetry 2> /dev/null)
GLOBAL_GIT := $(shell command -v git 2> /dev/null)
GLOBAL_PYENV := $(shell command -v pyenv 2> /dev/null)

PYTHON_TARGET_VERSION := 3.11.6

# Paths
VENV_DIRECTORY := ${PWD}/.venv
GIT_DIRECTORY := ${PWD}/.git
HOOKS_DIRECTORY := ${GIT_DIRECTORY}/hooks

# Files to Monitor
PYPROJECT := ${PWD}/pyproject.toml
POETRY_LOCK := ${PWD}/poetry.lock
PRE_COMMIT_CONFIG := ${PWD}/.pre-commit-config.yaml
PYVENV_CONFIG := ${VENV_DIRECTORY}/pyvenv.cfg
DEV_INSTALLED := ${VENV_DIRECTORY}/.dev_installed
INSTALLED := ${VENV_DIRECTORY}/.installed
REQUIREMENTS := ${PWD}/requirements.txt
MKDOCS_YAML := ${PWD}/mkdocs.yaml

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

clean:
	@rm -rf ${VENV_DIRECTORY}
	@rm -rf ${HOOKS_DIRECTORY}
	@${MAKE} -s _informative-message message="Virtual Environment and Hooks have been removed"

# Installation Rules

.PHONY: install
install:
	@${MAKE} -s ${INSTALLED}
	@${MAKE} -s ${GIT_DIRECTORY}
	@${MAKE} -s _informative-message message="To run a command within poetry's environment, prefix it with 'poetry run'"

.PHONY: install-dev
install-dev:
	@${MAKE} -s ${DEV_INSTALLED}
	@${MAKE} -s ${GIT_DIRECTORY}
	@${MAKE} -s ${HOOKS_DIRECTORY}
	@${MAKE} -s _informative-message message="To run a command within poetry's environment, prefix it with 'poetry run'"

# Pyenv Rules

.PHONY: check-pyenv
check-pyenv:
	@${MAKE} -s _starting-task-message message="Checking Pyenv Installation..."
	@if [ -z ${GLOBAL_PYENV} ]; then echo -e "Pyenv is not installed on your global python. Check 'https://github.com/pyenv/pyenv' to install pyenv."; exit 2 ;fi
	@${MAKE} -s _completed-task-message message="Valid Installation"

.PHONY: pyenv-install
_pyenv-install:
	@${MAKE} -s _starting-task-message message="Installing Python ${version} using Pyenv..."
	${GLOBAL_PYENV} install --skip-existing $(version)
	@${MAKE} -s _completed-task-message message="Installation Completed"

.PHONY: pyenv-local
_pyenv-local:
	@${MAKE} -s _starting-task-message message="Setting Python ${version} as local version..."
	${GLOBAL_PYENV} local $(version)
	@${MAKE} -s _completed-task-message message="Local Python Version Set to ${version} "

.PHONY: set-pyenv-up
set-pyenv-up: check-pyenv
	@${MAKE} -s _pyenv-install version=$(PYTHON_TARGET_VERSION)
	@${MAKE} -s _pyenv-local version=$(PYTHON_TARGET_VERSION)

# Poetry Rules

.PHONY: install-poetry
install-poetry:
	@${MAKE} -s _starting-task-message message="Installing Poetry..."
	@curl -sSL https://install.python-poetry.org | ${GLOBAL_PYTHON}
	@${MAKE} -s _completed-task-message message="Successful Installation of Poetry"

.PHONY: check-poetry
check-poetry: ${PYPROJECT}
	@${MAKE} -s _starting-task-message message="Checking Poetry Configuration..."
	@if [ -z ${GLOBAL_POETRY} ]; then echo -e "Poetry is not installed on your global python. Use 'make install-poetry' to install Poetry on your global python."; exit 2 ;fi
	@${MAKE} -s _completed-task-message message="Valid Configuration"

${PYVENV_CONFIG}:
	@${MAKE} -s set-pyenv-up
	@${MAKE} -s check-poetry
	@${MAKE} -s _starting-task-message message="Set up of Poetry's Python Version..."
	@${GLOBAL_POETRY} env use $(subst \,/, $(shell command ${GLOBAL_PYENV} which python))
	@${MAKE} -s _completed-task-message message="Set Up of Poetry's Python Version Completed."

${POETRY_LOCK}: ${PYVENV_CONFIG}
	@${MAKE} -s _starting-task-message message="Creating poetry.lock..."
	@${GLOBAL_POETRY} lock --no-update --ansi
	@${MAKE} -s _completed-task-message message="Created"

${INSTALLED}: ${POETRY_LOCK}
	@${MAKE} -s _starting-task-message message="Installing Main Dependencies..."
	@${GLOBAL_POETRY} install --without dev --ansi
	@touch ${INSTALLED}
	@${MAKE} -s _completed-task-message message="Successful Installation of Main Dependencies"

.PHONY: poetry-export
poetry-export: ${REQUIREMENTS}

${REQUIREMENTS}: ${POETRY_LOCK}
	@${MAKE} -s _starting-task-message message="Exporting Dependencies to requirements.txt..."
	@${GLOBAL_POETRY} export -f requirements.txt -o requirements.txt --without-hashes
	@${MAKE} -s _completed-task-message message="Successful Export"

# Development Rules

${DEV_INSTALLED}: ${POETRY_LOCK}
	@${MAKE} -s _starting-task-message message="Installing All Dependencies..."
	@${GLOBAL_POETRY} install --ansi
	@touch ${DEV_INSTALLED}
	@${MAKE} -s _completed-task-message message="Successful Installation of All Dependencies"

${HOOKS_DIRECTORY}: ${PRE_COMMIT_CONFIG} ${POETRY_LOCK} ${GIT_DIRECTORY}
	@${MAKE} -s _starting-task-message message="Installing Pre-Commit Hooks..."
	@${GLOBAL_POETRY} run pre-commit install
	@${MAKE} -s _completed-task-message message="Successful Installation of Hooks"

# Git

set-git-up:
	@${MAKE} -s ${GIT_DIRECTORY}

.PHONY: check-git
check-git:
	@${MAKE} -s _starting-task-message message="Checking Git Installation..."
	@if [ -z ${GLOBAL_GIT} ]; then echo -e "Git is not installed on your computer. Check 'https://git-scm.com/downloads' to install git."; exit 2 ;fi
	@${MAKE} -s _completed-task-message message="Valid Installation"

${GIT_DIRECTORY}:
	@${MAKE} -s check-git
	@${MAKE} -s _starting-task-message message="Git Repository Initialisation..."
	@${GLOBAL_GIT} init
	@${MAKE} -s _completed-task-message message="Repository Initialisation Completed"
	@${MAKE} -s enable-nbstripout

.PHONY: enable-nbstripout
enable-nbstripout: ${DEV_INSTALLED}
	@${MAKE} -s _starting-task-message message="Enabling nbstripout..."
	@${GLOBAL_POETRY} run nbstripout --install
	@${MAKE} -s _completed-task-message message="Enabled"

# Verbose

.PHONY: _starting-task-message
_starting-task-message:
	@echo -e "\n  ${CONSTRUCTION} ${PURPLE}$(message)${NOCOLOR} ${CONSTRUCTION}"

.PHONY: _completed-task-message
_completed-task-message:
	@echo -e "  ${VALID} ${GREEN}$(message)${NOCOLOR} ${VALID}"

.PHONY: _informative-message
_informative-message:
	@echo -e "  ${FIRE} ${BLUE}$(message)${NOCOLOR} ${FIRE}"
