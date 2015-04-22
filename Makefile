IMAGE_NAME=devcamp/blackjack-dealer-service
REPO_URL=registry.swg-devops.com
TAG=localtest

test: test-tdd test-bdd

test-tdd:
	@python -m unittest discover -p '*Test.py'

test-bdd:
	@behave

dockerbuild:
	@docker build -t $(IMAGE_NAME):$(TAG) .

dockerpush:
	@docker tag -f $(IMAGE_NAME):$(TAG) $(REPO_URL)/$(IMAGE_NAME):$(TAG)
	@docker push $(REPO_URL)/$(IMAGE_NAME):$(TAG)

.PHONY:  test test-tdd test-bdd