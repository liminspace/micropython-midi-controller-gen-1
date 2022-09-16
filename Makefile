.PHONY: help pre_commit clean_pycache collect mpy_compile detect upload reset_hard release

.DEFAULT_GOAL := release

help:
	@echo "Here can be some help"

pre_commit:
	pre-commit run --all-files

clean_pycache:
	find . | grep -E "(/__pycache__$$|\.pyc$$|\.pyo$$)" | xargs rm -vrf

collect:
	python -m tools.boardman collect

mpy_compile:
	python -m tools.boardman mpy-compile

detect:
	python -m tools.boardman detect

upload:
	python -m tools.boardman upload

reset_hard:
	python -m tools.boardman reset-hard

release: pre_commit clean_pycache collect mpy_compile upload reset_hard
