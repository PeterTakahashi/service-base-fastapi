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

resource "google_project_service" "enable_apis" {
  project  = var.project_id
  for_each = toset([
    "container.googleapis.com",
    "compute.googleapis.com",
    "sqladmin.googleapis.com",
    "servicenetworking.googleapis.com",
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com",
    "dns.googleapis.com",
  ])
  service = each.key

  disable_on_destroy = false
}

# Enable other APIs as needed

#
# 2. GKE Autopilot cluster
#
resource "google_container_cluster" "primary" {
  name             = "service-base-auth-${var.env}-ap-cluster"
  description      = "Autopilot GKE cluster for service-base-auth"
  project          = var.project_id
  location         = var.region
  enable_autopilot = true
  networking_mode  = "VPC_NATIVE"

  resource_labels = {
    environment = var.env
    team        = "infra"
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "google_compute_global_address" "private_ip_range" {
  name          = "private-ip-range"
  project       = var.project_id
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = "projects/${var.project_id}/global/networks/default"
}

# (2) VPC と GCPサービス (Service Networking) をピアリングする
resource "google_service_networking_connection" "default" {
  network                 = "projects/${var.project_id}/global/networks/default"
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_range.name]
}


#
# 3. Cloud SQL (PostgreSQL)
#
resource "google_sql_database_instance" "default" {
  name             = "service-base-auth-${var.env}-postgres"
  project          = var.project_id
  database_version = "POSTGRES_15"
  region           = var.region
  depends_on = [
    google_service_networking_connection.default
  ]

  settings {
    tier = "db-f1-micro"

    ip_configuration {
      ipv4_enabled    = false
      private_network = "projects/${var.project_id}/global/networks/default"
    }

    backup_configuration {
      enabled    = true
      start_time = "03:00"
    }
  }

  lifecycle {
    prevent_destroy = true
  }
}

# Create DB user
resource "google_sql_user" "users" {
  name     = "postgres"
  instance = google_sql_database_instance.default.name
  project  = var.project_id
  password = var.db_password

  depends_on = [
    google_sql_database_instance.default
  ]
}

# Create database (if needed)
resource "google_sql_database" "appdb" {
  name     = "fastapi_${var.env}"
  instance = google_sql_database_instance.default.name
  project  = var.project_id

  depends_on = [
    google_sql_database_instance.default
  ]
}
