IMAGE_NAME=devcamp/blackjack-dealer-service
REPO_URL=registry.swg-devops.com
TAG=localtest

test: test-unit test-integration

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
	docker -H ${DOCKER_HOST} kill ${ETCD_NAME}
	docker -H ${DOCKER_HOST} rm ${ETCD_NAME}

.PHONY: test test-unit test-integration dockerbuild dockerpush clean
