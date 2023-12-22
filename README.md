# Bot for solving python questions

## Run bot

### Without Docker
**Dependencies:**

- postgres
- golang-migrate (https://github.com/golang-migrate/migrate)
- poetry (https://python-poetry.org)

**Create .env with:**
```
PG_HOST=
PG_PORT=
PG_USER=
PG_PASSWORD=
PG_DATABASE=

TOKEN=
```

**Install libs:**
```
poetry install
```

**Apply migrations**
```
migrate -path ./migrations -database "postgres://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}?sslmode=disable" up
```

### With Docker
Build image:
```
docker build --no-cache -t python-problems-bot .
```

Change in docker-compose.yml env vars and:
```
docker-compose up -d --no-deps
```



## Development

### Create migrations
```
migrate create -ext sql -dir migrations {migration-name} 
```


### Linter:
```
poetry run ruff check . --fix
```

### Unit Tests:
```
pytest -v tests
```

### Functional Tests:
**Run postgres for tests**
```
docker run --name postgres-ppb -e POSTGRES_USER=python-problems-bot -e POSTGRES_PASSWORD=python-problems-bot -e POSTGRES_DB=python-problems-bot -p 5432:5432 -d postgres
```
**Apply migrations**
```
migrate -path ./migrations -database "postgres://python-problems-bot:python-problems-bot@localhost:5432/python-problems-bot?sslmode=disable" up
```
**Apply migrations**
```
pytest -v tests_functional
```
**Stop postgres for tests**
```
docker stop postgres-ppb
```
