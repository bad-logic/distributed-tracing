## Consumer for kafka Events

#### TECH STACK

- Language C++
- PackageManager [conan](https://docs.conan.io/en/latest/getting_started.html)

### Intended working principle

- Run this service as a sidecar service for any service that needs to consume events from another service
- Provide a list of Events to listen and api to hit while consuming those events. [here](./configs/routes.yaml)

Applications README\
[product microservice](../products/README.md)\
[order microservice](../orders/README.md)\
[consumer node](../consumer-node/README.md)
