## Consumer for kafka Events

#### TECH STACK

- Language Javascript
- Runtime NodeJS
- Package Manager pnpm

### Intended working principle

- Run this service as a sidecar service for any service that needs to consume events from another service
- Provide a list of Events to listen and api to hit while consuming those events. [here](./configs/listeners.yaml)

Applications README\
[product microservice](../products/README.md)\
[order microservice](../orders/README.md)\
[consumer cpp](../consumers/README.md)
