distribute:
	[ -z $(ls dist/)  ] || rm dist/*
	python3 setup.py bdist
	python3 setup.py bdist_wheel
	twine upload -u jurismarches -s dist/*
