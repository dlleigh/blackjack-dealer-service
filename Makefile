IMAGE_NAME=devcamp/blackjack-dealer-service
REPO_URL=registry.swg-devops.com
TAG=localtest

test: clean test-unit test-integration

test-unit:
	@python -m unittest discover -p '*Test.py'

test-integration:
	docker -H ${DOCKER_HOST} run --name ${ETCD_NAME} -d -p 8001:8001 -p ${ETCD_PORT}:${ETCD_PORT} quay.io/coreos/etcd:v0.4.6 -peer-addr 127.0.0.1:8001 -addr 127.0.0.1:2379
	behave #--no-capture -D BEHAVE_DEBUG_ON_ERROR --tags=-etcd
	docker -H ${DOCKER_HOST} kill ${ETCD_NAME}
	docker -H ${DOCKER_HOST} rm ${ETCD_NAME}

dockerbuild:
	@docker build -t $(IMAGE_NAME):$(TAG) .

dockerpush:
	@docker tag -f $(IMAGE_NAME):$(TAG) $(REPO_URL)/$(IMAGE_NAME):$(TAG)
	@docker push $(REPO_URL)/$(IMAGE_NAME):$(TAG)

clean:
	docker -H ${DOCKER_HOST} kill ${ETCD_NAME} | true
	docker -H ${DOCKER_HOST} rm ${ETCD_NAME} | true

deploy:
	@docker pull $(REPO_URL)/$(IMAGE_NAME):$(TAG)
	@docker run -d -P --name blackjack-dealer-service-$(TAG) $(REPO_URL)/$(IMAGE_NAME):$(TAG)
	@docker ps | grep blackjack-dealer-service- | grep -v blackjack-dealer-service-$(TAG) | cut -f1 -d' ' | xargs -r docker stop
	@docker ps -f status=exited | grep blackjack-dealer-service- | cut -f1 -d' ' | xargs -r docker rm

dependencies:
	@sudo pip install -r requirements.txt

.PHONY: test test-unit test-integration dockerbuild dockerpush clean dependencies
