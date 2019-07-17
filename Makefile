.PHONY: clean-pyc

help:
	@echo "    init"
	@echo "        Installs necessary dependencies"
	@echo "    shell"
	@echo "        Enters Python virtual environment"
	@echo "    clean-pyc"
	@echo "        Remove python artifacts."
	@echo "    lint"
	@echo "        Run lint script on application."
	@echo "    test"
	@echo "        Run py.test"
	@echo "    test-ci"
	@echo "        Runs lint and test."

init:
	@pip install -r requirements.txt

shell:
	@pipenv shell

clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

lint:
	@./scripts/lint

test:
	@./scripts/test
	@$(MAKE) clean-pyc

lint-test: lint test
