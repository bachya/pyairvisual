coverage:
	pipenv run py.test -s --verbose --cov-report term-missing --cov-report xml --cov=pyairvisual tests
init:
	pip install --upgrade pip pipenv
	pipenv lock
	pipenv install --dev
lint:
	pipenv run flake8 pyairvisual
	pipenv run pydocstyle pyairvisual
	pipenv run pylint pyairvisual
publish:
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*
	rm -rf dist/ build/ .egg pyairvisual.egg-info/
test:
	pipenv run py.test
