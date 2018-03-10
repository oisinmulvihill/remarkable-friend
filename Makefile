
test_install:
	pipenv run pip install -r test-requirements.txt

test: test_install
	pipenv run pytest --cov=rmfriend

install:
	pipenv install
	pipenv run python setup.py develop
