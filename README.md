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

#### create db migration file

```bash
alembic revision --autogenerate -m ""
```

#### db migrate

```bash
alembic upgrade head
```

#### reset table

```bash
docker compose down -v
```

#### create schema

```bash
python -m scripts.create_schema
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

## deployment

### terraform

```
export TF_VAR_project_id=""
export TF_VAR_db_password=""

terraform init
terraform plan
terraform apply
```

```
gcloud iam service-accounts keys create service-account-key.json \
  --iam-account=service-base-deployment-user@{PROJECT_ID}.iam.gserviceaccount.com
export GOOGLE_APPLICATION_CREDENTIALS=./service-account-key.json
```
