# Service Base FastAPI

## Installation

### Local setup

#### Docker

```bash
docker exec -it service-base-web bash
source .venv/bin/activate

pytest --cov=app --cov-report=term-missing --cov-report=html
open htmlcov/index.html # if you wanna see cov report

open http://localhost:1080 # open mail log
open http://127.0.0.1:8000/app/v1/docs # open api docs

```

### start stripe local server

```sh
stripe listen --events=payment_intent.succeeded --forward-to http://127.0.0.1:8000/app/v1/payment-intents/webhook
```

ref: https://docs.stripe.com/cli/listen
stripe test card: https://docs.stripe.com/testing

### reset db

```
docker compose down -v
docker compose up -d
docker exec -it service-base-web bash
source .venv/bin/activate
alembic revision --autogenerate -m "init"
alembic upgrade head
ENV=test alembic upgrade head
```

#### create db migration file

```bash
alembic revision --autogenerate -m ""
```

#### db migrate

for development

```bash
alembic upgrade head
ENV=test alembic upgrade head
```

#### reset table

```bash
docker compose down -v
```

#### create schema

```bash
python -m scripts.create_schema
python scripts/generate_repositories_from_models.py
python scripts/generate_repository_dependencies.py
python scripts/generate_repository_fixtures.py
```

#### code formatter

```
black .
ruff check . --fix
```

#### code checker

```
ruff check .
mypy --config-file mypy.ini .
```

#### OpenAPI

html
http://0.0.0.0:8000/app/v1/docs#/

json
http://0.0.0.0:8000/app/v1/openapi.json

#### Admin Console

http://127.0.0.1:8000/admin/login
