distribute:
	if [ -z "$(ls dist/)"  ]; then rm dist/*; fi
	python3 setup.py sdist
	# see https://github.com/pypa/wheel/issues/99#issuecomment-317885424
	# we want to exclude tests
	pip wheel --no-index --no-deps --wheel-dir dist dist/*.tar.gz
	twine upload -u jurismarches -s dist/*
