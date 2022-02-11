.PHONY: clean build publish

build: clean
	python3 -m pip install --upgrade --quiet build twine
	python3 -m build

publish: build
	python3 -m twine check dist/*
	python3 -m twine upload dist/*

clean:
	rm -r dist *.egg-info || true
	find rapidunfurl/ -type d -name '__pycache__' -exec rm -rf {} \;
