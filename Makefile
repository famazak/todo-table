.PHONY: test
test:
	poetry run pytest

.PHONY: build
build:
	poetry build

.PHONY: publish
publish:
	poetry publish --build
