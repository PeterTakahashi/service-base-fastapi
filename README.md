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

#### create iam and attach role

create service user

```sh
cd terraform/infra
gcloud iam service-accounts create service-base-deployment-user \
  --display-name "Service Account for CI deployment"
```

```sh
SERVICE_ACCOUNT_EMAIL=$(gcloud iam service-accounts list \
  --filter="displayName:Service Account for CI deployment" \
  --format="value(email)")

ROLES=(
  "roles/container.developer"
  "roles/compute.viewer"
  "roles/iam.serviceAccountUser"
  "roles/container.clusterViewer"
  "roles/iam.serviceAccountAdmin"
  "roles/container.admin"
  "roles/servicenetworking.networksAdmin"
  "roles/compute.networkAdmin"
  "roles/cloudsql.admin"
)

GCP_PROJECT_ID="aiproject-460606"

for ROLE in "${ROLES[@]}"; do
  gcloud projects add-iam-policy-binding "$GCP_PROJECT_ID" \
    --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
    --role="$ROLE"
done
```

```sh
gcloud iam service-accounts keys create service-account-key.json \
  --iam-account="$SERVICE_ACCOUNT_EMAIL"
export GOOGLE_APPLICATION_CREDENTIALS=./service-account-key.json
```

#### change resource

```sh
export TF_VAR_project_id="aiproject-460606"
export TF_VAR_db_password=""

terraform init
terraform plan
terraform apply
```
