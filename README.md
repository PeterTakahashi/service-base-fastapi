# Image/Manga Translator

## Installation

### Local setup

#### Docker

```bash
docker exec -it manga-translator-web bash
source .venv/bin/activate

pytest --cov=app --cov-report=term-missing --cov-report=html
```

create db migration file

```bash
alembic revision --autogenerate -m ""
```

db migrate

```bash
alembic upgrade head
```

reset table

```bash
docker compose down -v
```

create schema

```bash
python -m scripts.create_schema
```

code formatter
```
black .
ruff check . --fix
```

#### OpenAPI

html
http://0.0.0.0:8000/app/v1/docs#/

json
http://0.0.0.0:8000/app/v1/openapi.json
