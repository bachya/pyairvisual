ci:
	pipenv run py.test --junitxml=report.xml
coverage:
	pipenv run py.test -s --verbose --cov-report term-missing --cov-report xml --cov=pyden tests
docs:
	cd docs && make html
flake8:
	pipenv run flake8 pyden
init:
	pip install --upgrade pip pipenv
	pipenv lock
	pipenv install --dev
publish:
	python setup.py publish
	rm -rf dist/ build/ .egg pyden.egg-info/
test:
	pipenv run detox
