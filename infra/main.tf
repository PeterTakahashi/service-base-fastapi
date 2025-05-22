#
# 1. Enable required APIs
#
resource "google_project_service" "enable_container" {
  project = var.project_id
  service = "container.googleapis.com"
}

resource "google_project_service" "enable_sqladmin" {
  project = var.project_id
  service = "sqladmin.googleapis.com"
}

resource "google_project_service" "enable_iam" {
  project = var.project_id
  service = "iam.googleapis.com"
}

# Enable other APIs as needed

#
# 2. GKE Autopilot cluster
#
resource "google_container_cluster" "primary" {
  name     = "service-base-auth-autopilot-cluster"
  project  = var.project_id
  location = var.region

  enable_autopilot = true

   # Use default network or create and specify a VPC if needed
  networking_mode = "VPC_NATIVE"
}

#
# 3. Cloud SQL (PostgreSQL)
#
resource "google_sql_database_instance" "default" {
  name             = "service-base-auth-postgres"
  project          = var.project_id
  database_version = "POSTGRES_17"  # Version supported by GCP
  region           = var.region

  settings {
    tier = "db-f1-micro" #  Smallest tier for testing
  }
}

# Create DB user
resource "google_sql_user" "users" {
  name     = "postgres"
  instance = google_sql_database_instance.default.name
  project  = var.project_id
  password = var.db_password
}

# Create database (if needed)
resource "google_sql_database" "appdb" {
  name     = "fastapi_production"
  instance = google_sql_database_instance.default.name
  project  = var.project_id
}
