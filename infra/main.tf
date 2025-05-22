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
    # --- Compute/GKE 関連 ---
    # GKEクラスタ本体 (container.googleapis.com は必須)
    "container.googleapis.com",
    # VPC やロードバランサなどインフラまわりで必要 (特にPrivate IPの設定時)
    "compute.googleapis.com",
    # --- Cloud SQL 関連 ---
    # Cloud SQL for PostgreSQL/MySQL/SQL Server を扱うため
    "sqladmin.googleapis.com",
    # Private IP 接続などで VPC ピアリングを行う際に必要
    "servicenetworking.googleapis.com",

    # --- IAM 関連 ---
    # サービスアカウント、ロールの管理
    "iam.googleapis.com",
    # Cloud Resource Manager API (追加でロールバインディングなど行う場合に必要)
    "cloudresourcemanager.googleapis.com",

    # --- ログ・モニタリング ---
    # Stackdriver Logging, Cloud Monitoring
    "logging.googleapis.com",
    "monitoring.googleapis.com",

    # --- DNS  ---
    # Cloud DNS を使って独自ドメイン運用するなら必要
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
