test: test-tdd test-bdd

test-tdd:
	@python -m unittest discover -p '*Test.py'

test-bdd:
	@behave


.PHONY:  test test-tdd test-bdd