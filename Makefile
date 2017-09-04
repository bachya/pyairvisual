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
	pipenv run python setup.py publish
test:
	pipenv run detox
