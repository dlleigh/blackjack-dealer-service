## Get Started

#### Install dependencies
```
virtualenv .
source bin/activate
pip install -r requirements.txt
```

#### Environment Dependencies
```
$ export ETCD_ENDPOINT=...
$ export DEALER_UUID=...
$ export DEALER_ENDPOINT=...
```

#### Run it
```
$ python BlackJackDealerService.py
```

## Tests

#### Environment Dependencies (in additon to runtime deps above)
```
$ export DOCKER_HOST=...
$ export ETCD_ENDPOINT=192.168.59.103:2379
$ export ETCD_NAME=etcd-0
$ export ETCD_PORT=2379
```

#### All
```
make tests
```

#### Unit
```
make tests-unit
```

#### Integration
**NOTE**: integration `make` steps depend on `docker` cli to manage containers of various service dependencies (i.e. `etcd`)
```
make tests-integration
```