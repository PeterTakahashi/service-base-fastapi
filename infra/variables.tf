variable "project_id" {
  type        = string
  description = "aiproject-460606"
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
