for migration alembic is used

go to the shell of your docker container
go to /src folder

poetry add <package_name>
poetry remove <package_name>

FOR MIGRATIONS

```
alembic init <folder_name>
```

this will generate the setup for migrations

run

```
alembic revision -m "creating_the_order_table"
alembic revision --autogenerate -m "creating_the_order_table"
```

for auto generate please update the target_metadata array in migrations/env.py

this will generate a migration file inside alembic/versions/

run

```
alembic upgrade head
```

to run the migrations
