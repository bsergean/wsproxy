all: flake

dev:
	@echo "--> Installing Python dependencies"
	# order matters here, base package must install first
	pip install -U pip
	pip install --requirement requirements.txt
	pip install --requirement tests/requirements.txt
	pip install -e .
	pip install "file://`pwd`#egg=wsproxy[dev]"

upload:
	rm -rf dist/*
	python setup.py sdist bdist_wheel
	twine upload dist/*.whl
	rm -rf build/

lint: flake

indent:
	black -S wsproxy tests

format: indent

flake:
	flake8 --max-line-length=88 `find wsproxy -name '*.py'`

test:
	py.test -n 4 --disable-warnings tests/*.py

mypy:
	mypy --ignore-missing-imports wsproxy/*.py

pylint:
	pylint -E -j 10 -r n -d C0301 -d C0103 -d C0111 -d C0330 -d W1401 -d W1203 -d W1202 `find wsproxy -name '*.py'`

coverage:
	py.test -n 4 --disable-warnings --cov=wsproxy --cov-report html --cov-report term tests

isort:
	isort `find wsproxy tests -name '*.py'`

release:
	git commit -am 'bump' ; git push ; make upload

# this is helpful to remove trailing whitespaces
trail:
	test `uname` = Linux || sed -E -i '' -e 's/[[:space:]]*$$//' `find src tests -name '*.py'`
	test `uname` = Darwin || sed -i 's/[ \t]*$$//' `find src tests -name '*.py'`

#  python -m venv venv
#  source venv/bin/activate
#  pip install mkdocs
doc:
	mkdocs gh-deploy

clean:
	find . -name __pycache__ -exec rm -rf {} \;
	find . -name __pycache__ -delete
	find wsproxy tests -name '*.pyc' -delete
	rm -f *.pyc
	rm -rf wsproxy.egg-info
	rm -rf build
