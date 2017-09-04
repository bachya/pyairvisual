ci:
	pipenv run py.test --junitxml=report.xml
coverage:
	pipenv run py.test -s --verbose --cov-report term-missing --cov-report xml --cov=pyairvisual tests
docs:
	cd docs && make html
init:
	pip install --upgrade pip pipenv
	pipenv lock
	pipenv install --dev
lint:
	pipenv run flake8 pyairvisual
	pipenv run pydocstyle pyairvisual
publish:
	python setup.py publish
	rm -rf dist/ build/ .egg pyden.egg-info/
test:
	pipenv run detox
