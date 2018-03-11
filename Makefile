
test_install:
	pip install -r test-requirements.txt

test: test_install
	pytest --cov=rmfriend

install:
	pip install -r requirements.txt
	python setup.py develop
