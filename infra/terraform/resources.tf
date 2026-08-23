# ==============================================================================
# Monchis Café — Recursos de Infraestructura en Google Cloud Platform (IaC)
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. Google Secret Manager (Almacenamiento Seguro de Credenciales)
# ------------------------------------------------------------------------------
resource "google_secret_manager_secret" "jwt_access_secret" {
  secret_id = "monchis-jwt-access-secret"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "jwt_access_secret_ver" {
  secret      = google_secret_manager_secret.jwt_access_secret.id
  secret_data = var.jwt_access_secret
}

resource "google_secret_manager_secret" "recaptcha_secret" {
  secret_id = "monchis-recaptcha-secret"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "recaptcha_secret_ver" {
  secret      = google_secret_manager_secret.recaptcha_secret.id
  secret_data = var.recaptcha_secret_key
}

# ------------------------------------------------------------------------------
# 2. Google Cloud SQL (PostgreSQL Gestionado para Monchis Café)
# ------------------------------------------------------------------------------
resource "google_sql_database_instance" "postgres_instance" {
  name             = "monchis-cafe-postgres-${var.environment}"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-f1-micro" # Escalable para producción
    ip_configuration {
      ipv4_enabled = true
    }
    backup_configuration {
      enabled = true
    }
  }
  deletion_protection = false
}

resource "google_sql_database" "database" {
  name     = "monchis_db"
  instance = google_sql_database_instance.postgres_instance.name
}

resource "google_sql_user" "db_user" {
  name     = "monchis_admin"
  instance = google_sql_database_instance.postgres_instance.name
  password = var.db_password
}

# ------------------------------------------------------------------------------
# 3. Google Cloud Memorystore (Redis Gestionado para Rate-Limiting y Caché)
# ------------------------------------------------------------------------------
resource "google_redis_instance" "cache" {
  name           = "monchis-redis-${var.environment}"
  tier           = "BASIC"
  memory_size_gb = 1
  region         = var.region
  redis_version  = "REDIS_7_0"
}

# ------------------------------------------------------------------------------
# 4. Google Cloud Run — Backend API (Next.js API Gateway & Microservicios)
# ------------------------------------------------------------------------------
resource "google_cloud_run_v2_service" "api_service" {
  name     = "monchis-api-${var.environment}"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "gcr.io/${var.project_id}/monchis-api:latest"
      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
      env {
        name  = "NODE_ENV"
        value = "production"
      }
      env {
        name  = "DATABASE_URL"
        value = "postgresql://monchis_admin:${var.db_password}@${google_sql_database_instance.postgres_instance.public_ip_address}:5432/monchis_db?schema=public"
      }
      env {
        name  = "REDIS_URL"
        value = "redis://${google_redis_instance.cache.host}:${google_redis_instance.cache.port}"
      }
    }
  }
}

# ------------------------------------------------------------------------------
# 5. Google Cloud Run — Frontend Web (Vue 3 + ViteSSG)
# ------------------------------------------------------------------------------
resource "google_cloud_run_v2_service" "web_service" {
  name     = "monchis-web-${var.environment}"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "gcr.io/${var.project_id}/monchis-web:latest"
      resources {
        limits = {
          cpu    = "1"
          memory = "256Mi"
        }
      }
      env {
        name  = "VITE_API_URL"
        value = google_cloud_run_v2_service.api_service.uri
      }
    }
  }
}

# ------------------------------------------------------------------------------
# 6. Accesos Públicos IAM para Cloud Run
# ------------------------------------------------------------------------------
resource "google_cloud_run_service_iam_binding" "public_web" {
  location = google_cloud_run_v2_service.web_service.location
  service  = google_cloud_run_v2_service.web_service.name
  role     = "roles/run.invoker"
  members  = ["allUsers"]
}

resource "google_cloud_run_service_iam_binding" "public_api" {
  location = google_cloud_run_v2_service.api_service.location
  service  = google_cloud_run_v2_service.api_service.name
  role     = "roles/run.invoker"
  members  = ["allUsers"]
}

# ------------------------------------------------------------------------------
# 7. Cloud Armor Security Policy (WAF & DDoS Mitigation)
# ------------------------------------------------------------------------------
resource "google_compute_security_policy" "cloud_armor_policy" {
  name        = "monchis-cloud-armor-policy"
  description = "Reglas WAF de Cloud Armor para protección de Monchis Café"

  rule {
    action   = "allow"
    priority = "2147483647"
    match {
      versioned_expr = "SRC_IPS_V1"
      config {
        src_ip_ranges = ["*"]
      }
    }
    description = "Regla por defecto de acceso"
  }

  rule {
    action   = "rate_based_ban"
    priority = "1000"
    match {
      versioned_expr = "SRC_IPS_V1"
      config {
        src_ip_ranges = ["*"]
      }
    }
    rate_limit_options {
      conform_action = "allow"
      exceed_action  = "deny(429)"
      rate_limit_threshold {
        count        = 120
        interval_sec = 60
      }
      ban_duration_sec = 300
    }
    description = "Mitigación de ataques de fuerza bruta y DDoS (Máx 120 peticiones/minuto por IP)"
  }
}
