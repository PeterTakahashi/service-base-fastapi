terraform {
  required_version = ">= 1.3.0"

  backend "gcs" {
    bucket = "aiproject-terraform-state"
    prefix = "infra/terraform.tfstate"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.61"
    }

    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.22"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

provider "kubernetes" {
}
