variable "project_id" {
  type        = string
  description = "GCP project ID"
}

variable "region" {
  type        = string
  default     = "us-central1"
}

variable "zone" {
  type        = string
  default     = "us-central1-a"
}

variable "db_password" {
  type        = string
  description = "PostgreSQL password"
  sensitive   = true
}

variable "env" {
  type    = string
  default = "production"
}

variable "github_oauth_client_id" {
  type        = string
  description = "GitHub OAuth Client ID"
}

variable "github_oauth_client_secret" {
  type        = string
  description = "GitHub OAuth Client Secret"
  sensitive   = true
}

variable "google_oauth_client_id" {
  type        = string
  description = "Google OAuth Client ID"
}

variable "google_oauth_client_secret" {
  type        = string
  description = "Google OAuth Client Secret"
  sensitive   = true
}