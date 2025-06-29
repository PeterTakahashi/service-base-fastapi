# Service Base FastAPI

<img src="docs/img/front/home.png" width="700" />

## Installation

### Get Start on local

```sh
# start backend
git clone
cp .env.example .env
docker compose up
docker exec -it service-base-web bash
source .venv/bin/activate
alembic upgrade head
ENV=test alembic upgrade head

# start frontend
git clone
npm install
cp .env.example .env
npm run dev

# start stripe local server
# ref: https://docs.stripe.com/cli/listen
# stripe test card: https://docs.stripe.com/testing
stripe listen --events=payment_intent.succeeded --forward-to http://127.0.0.1:8000/app/v1/payment-intents/webhook

```

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
local: http://localhost:8000/app/v1/docs
server: https://service-base-fastapi-swagger.vercel.app

json
local: http://0.0.0.0:8000/app/v1/openapi.json
server: https://raw.githubusercontent.com/PeterTakahashi/service-base-fastapi/refs/heads/main/docs/openapi.json

http://127.0.0.1:8000/admin/login
username: `admin`
password: `password`

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
  "roles/storage.admin"
  "roles/cloudsql.client"
  "roles/cloudsql.viewer"
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

### bucket create for remaining terraform state

```sh
gsutil mb -p $GCP_PROJECT_ID -l us-central1 gs://aiproject-terraform-state/
```

#### change resource

```sh
export TF_VAR_project_id="aiproject-460606"
export TF_VAR_db_password=""
export TF_VAR_github_oauth_client_id=""
export TF_VAR_github_oauth_client_secret=""
export TF_VAR_google_oauth_client_id=""
export TF_VAR_google_oauth_client_secret=""
export TF_VAR_docker_username=""
export TF_VAR_docker_password=""
export TF_VAR_docker_email=""

gcloud container clusters get-credentials service-base-auth-ap-cluster \
  --region us-central1 \
  --project aiproject-460606

terraform init
terraform plan
terraform apply
```

## screan shots

### SignIn

<img src="docs/img/front/signin.png" width="700" />

### Account

<img src="docs/img/front/account.png" width="700" />

### Add Funds

<img src="docs/img/front/addfunds.png" width="700" />

### API Key List

<img src="docs/img/front/apikeylist.png" width="700" />

### Create API Key

<img src="docs/img/front/createapikey.png" width="700" />

### Edit Email

<img src="docs/img/front/editemail.png" width="700" />

### Forgot Password

<img src="docs/img/front/forgotpassword.png" width="700" />

### Home

<img src="docs/img/front/home.png" width="700" />

### Input Card

<img src="docs/img/front/inputcard.png" width="700" />

### Sign Up

<img src="docs/img/front/signup.png" width="700" />

### Transactions

<img src="docs/img/front/transactions.png" width="700" />

### Wallet

<img src="docs/img/front/wallet.png" width="700" />
