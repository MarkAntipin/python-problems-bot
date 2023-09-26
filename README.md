# Bot for solving python questions

## Run bot

### Without Docker
**Dependencies:**

- postgres
- mongo
- golang-migrate (https://github.com/golang-migrate/migrate)
- poetry (https://python-poetry.org)

**Create .env with:**
```
PG_HOST=
PG_PORT=
PG_USER=
PG_PASSWORD=
PG_DATABASE=

MONGO_HOST==
MONGO_PORT=
MONGO_USER=
MONGO_PASSWORD=
MONGO_DATABASE=

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

Change in docker-compose.yml env vars and:
```
docker-compose up -d --no-deps --build
```



## Development

**Linter**:
```
poetry run ruff check . --fix
```

**Tests**:
- **create test bot in @BotFather**
- **run test bot**
```
TOKEN={YOUR_TEST_BOT_TOKEN} docker-compose -f docker-compose.test.yml  up  --build
```
- **get API_ID and API_ID throw https://my.telegram.org**
- **get session string with [get_session_for_tests.py](tools%2Fget_session_for_tests.py) script**
- **Add in .env:**
```
TEST_TELEGRAM_APP_ID=
TEST_TELEGRAM_APP_HASH=
TEST_TELETHON_SESSION=
TEST_BOT_NAME=
```
- **run tests**
```
pytest -v tests
```
- **stop test bot**
```
docker-compose -f docker-compose.test.yml  down 
```
