# Bot for solving python questions
https://t.me/python_problems_bot


## Backend Development (backend folder)
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
PAYMENT_PROVIDER_TOKEN=
```

**Install libs:**
```
poetry install
```

**Up postgres**
```
createdb {PG_DATABASE}
```

or with docker:
```
docker run --name postgres-ppb -e POSTGRES_USER={PG_USER} -e POSTGRES_PASSWORD={PG_PASSWORD} -e POSTGRES_DB={PG_DATABASE} -p 5436:5432 -d postgres
```


**Apply migrations**
```
migrate -path backend/migrations -database "postgres://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}?sslmode=disable" up
```

**Run bot**
```
poetry run python run_bot.py
```

**Run app**
```
poetry run python run_app.py
```

**Run scheduler**
```
poetry run python run_scheduler.py
```


## Backend Development

### Create migrations
```
migrate create -ext sql -dir backend/migrations {migration-name} 
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
docker run --name postgres-ppb -e POSTGRES_USER=python-problems-bot -e POSTGRES_PASSWORD=python-problems-bot -e POSTGRES_DB=python-problems-bot -p 5436:5432 -d postgres
```
**Apply migrations**
```
migrate -path backend/migrations -database "postgres://python-problems-bot:python-problems-bot@localhost:5436/python-problems-bot?sslmode=disable" up
```
**Run functional tests**
```
pytest -v tests_functional
```
**Stop postgres for tests**
```
docker stop postgres-ppb
```


## Frontend Development (frontend folder)
**Dependencies:**

- install ngrok (https://ngrok.com/) or analog

**Install libs:**
```
npm install
```

**Run Web App**
```
npm run dev
```

**Run Backend**
```
cd ../backend
poetry run python run_app.py
```

**Get ngrok frontend url**
```
ngrok http 5173
```

**Get ngrok backend url (you can use 2 different free accounts)**
```
ngrok http 3779
```

**Create .env with:**
```
VITE_REACT_APP_API_URL={backend_ngrock_url}
```

**Update Web App URL in @BotFather**


## Deploy
Build images:
```
docker build --no-cache -t python-problems-bot backend
```
and
```
docker build --no-cache -t python-problems-bot-frontend frontend
```

create .env file, look at .env.example
and run docker-compose
```
docker-compose up -d --no-deps
```
