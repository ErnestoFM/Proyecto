# ==============================================================================
# Monchis Café — Infraestructura como Código (Terraform - Google Cloud Platform)
# ==============================================================================

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

variable "project_id" {
  description = "GCP Project ID"
  type        = string
  default     = "monchis-cafe-prod"
}

variable "region" {
  description = "GCP Region for deployment"
  type        = string
  default     = "us-central1"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# --- Cloud SQL: PostgreSQL 15 ---
resource "google_sql_database_instance" "postgres_instance" {
  name             = "monchis-postgres-instance"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-f1-micro"
    backup_configuration {
      enabled = true
    }
    ip_configuration {
      ipv4_enabled = true
    }
  }
}

resource "google_sql_database" "database" {
  name     = "cafeteria_db"
  instance = google_sql_database_instance.postgres_instance.name
}

# --- Cloud Memorystore: Redis ---
resource "google_redis_instance" "cache" {
  name           = "monchis-redis-cache"
  tier           = "BASIC"
  memory_size_gb = 1
  region         = var.region
}

# --- Google Secret Manager: Custodia de Secretos ---
resource "google_secret_manager_secret" "jwt_secret" {
  secret_id = "JWT_ACCESS_SECRET"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "recaptcha_secret" {
  secret_id = "RECAPTCHA_SECRET_KEY"
  replication {
    auto {}
  }
}

# --- Cloud Run: Backend Next.js API ---
resource "google_cloud_run_v2_service" "api_service" {
  name     = "monchis-api"
  location = var.region

  template {
    containers {
      image = "gcr.io/${var.project_id}/monchis-api:latest"
      ports {
        container_port = 8080
      }
      env {
        name  = "NODE_ENV"
        value = "production"
      }
    }
  }
}

# --- Cloud Run: Frontend Vue 3 SPA ---
resource "google_cloud_run_v2_service" "web_service" {
  name     = "monchis-web"
  location = var.region

  template {
    containers {
      image = "gcr.io/${var.project_id}/monchis-web:latest"
      ports {
        container_port = 3000
      }
    }
  }
}
