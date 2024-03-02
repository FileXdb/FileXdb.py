ifeq ($(OS), Windows_NT)
build:
	python -m pip install --upgrade build
	python -m build

clean:
	# if exist "./build" rd /s /q build
	if exist "./dist" rd /s /q dist
	if exist "./filexdb.egg-info" rd /s /q filexdb.egg-info

clean-build:
	# if exist "./build" rd /s /q build
	if exist "./dist" rd /s /q dist
	if exist "./filexdb.egg-info" rd /s /q filexdb.egg-info

	python -m pip install --upgrade build
	python -m build

test-release:
	python -m pip install --upgrade twine
	python -m twine upload --repository testpypi dist/*

release:
	python -m pip install --upgrade twine
	python -m twine upload --skip-existing dist/*



else	# Linux or MAC
build:
	python3 -m pip install --upgrade build
	python3 -m build

clean:
	rm -rf build
	rm -rf dist
	rm -rf filexdb.egg-info

clean-build:
	rm -rf build
	rm -rf dist
	rm -rf filexdb.egg-info

	python3 -m build

test-release:
	python3 -m pip install --upgrade twine
	python3 -m twine upload --repository testpypi dist/*

release:
	python3 -m pip install --upgrade twine
	python3 -m twine upload dist/*


endif

#pypi-AgEIcHlwaS5vcmcCJDk5YjczZWY3LWIxNDAtNDE1ZC1iOTM3LTY3MTdmZjdhNTQ2MAACD1sxLFsiZmlsZXhkYiJdXQACLFsyLFsiMDUzOTY1MTQtZWU1OC00YzZmLTk0OWEtZGUzOWRhYTYyYzhhIl1dAAAGIE9ej3NpTEITK28hMaLoyloMCkS9ENOh0NZAt3R_rzAa