resource "google_project_service" "enable_container" {
  project = var.project_id
  service = "container.googleapis.com"
}

resource "google_project_service" "enable_iam" {
  project = var.project_id
  service = "iam.googleapis.com"
}

resource "google_project_service" "enable_apis" {
  project  = var.project_id
  for_each = toset([
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com",
  ])
  service = each.key

  disable_on_destroy = false
}

resource "google_service_account" "ci_user" {
  account_id   = "service-base-deployment-user"
  display_name = "Service Account for CI deployment"
}

locals {
  ci_roles = [
    "roles/container.developer",
    "roles/compute.viewer",
    "roles/iam.serviceAccountUser",
    "roles/container.clusterViewer",
    "roles/iam.serviceAccountAdmin",
    "roles/container.admin",
  ]
}

resource "google_project_iam_member" "ci_roles" {
  for_each = toset(local.ci_roles)

  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.ci_user.email}"
}
