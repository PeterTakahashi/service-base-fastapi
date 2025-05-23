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

variable "service_account_id" {
  type        = string
  description = "Service account ID"
  default = "service-base-deployment-user@aiproject-460606.iam.gserviceaccount.com"
}