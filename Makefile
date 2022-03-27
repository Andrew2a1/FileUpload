lint:
	python -W ignore -m autoflake --in-place --recursive --ignore-init-module-imports --remove-duplicate-keys --remove-unused-variables --remove-all-unused-imports .
	python -m black .
	python -m isort .
	python -m mypy . --ignore-missing-imports

run:
	python ./main.py