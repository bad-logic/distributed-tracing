## Order service

##### fetch, create, update and delete Order

##### Consume product events from product service

#### TECH STACK

- Language Python
- Database Mysql
- Package Manager Poetry
- Migration tool Alembic

MIGRATIONS SETUP

Initialize migration setup

```
alembic init <folder_name>
```

Create migration files

```
alembic revision -m "creating_the_order_table"
```

Autogenerate migration files from schema

```
alembic revision --autogenerate -m "creating_the_order_table"
```

> for auto generate please update the target_metadata array in migrations/env.py

Run Migrations

> To run migration commands you need to be same folder as `alembic.ini` file

```
alembic upgrade head
```

Revert Migrations

```
alembic downgrade -n
```

Applications README
[product microservice](../products/README.md)\
[consumer node](../consumer-node/README.md)\
[consumer cpp](../consumers/README.md)
