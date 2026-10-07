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
      require_ssl  = true
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

# ------------------------------------------------------------------------------
# 8. External HTTPS Application Load Balancer con Certificados SSL Gestionados
# y Conexión de Cloud Armor WAF a los Servicios Cloud Run
# ------------------------------------------------------------------------------

# 8.1 Certificado SSL Gestionado por Google (Auto-renovable)
resource "google_compute_managed_ssl_certificate" "lb_ssl_cert" {
  name = "monchis-managed-ssl-cert"
  managed {
    domains = [var.domain_name, "www.${var.domain_name}"]
  }
}

# 8.2 Serverless Network Endpoint Groups (NEGs) para Cloud Run
resource "google_compute_region_network_endpoint_group" "web_neg" {
  name                  = "monchis-web-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region
  cloud_run {
    service = google_cloud_run_v2_service.web_service.name
  }
}

resource "google_compute_region_network_endpoint_group" "api_neg" {
  name                  = "monchis-api-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region
  cloud_run {
    service = google_cloud_run_v2_service.api_service.name
  }
}

# 8.3 Backend Services (Vinculación con Política WAF de Cloud Armor)
resource "google_compute_backend_service" "web_backend" {
  name                  = "monchis-web-backend"
  protocol              = "HTTPS"
  security_policy       = google_compute_security_policy.cloud_armor_policy.id
  backend {
    group = google_compute_region_network_endpoint_group.web_neg.id
  }
}

resource "google_compute_backend_service" "api_backend" {
  name                  = "monchis-api-backend"
  protocol              = "HTTPS"
  security_policy       = google_compute_security_policy.cloud_armor_policy.id
  backend {
    group = google_compute_region_network_endpoint_group.api_neg.id
  }
}

# 8.4 URL Map (Enrutamiento /api/* a Backend y resto a Web Frontend)
resource "google_compute_url_map" "https_url_map" {
  name            = "monchis-https-url-map"
  default_service = google_compute_backend_service.web_backend.id

  host_rule {
    hosts        = ["*"]
    path_matcher = "allpaths"
  }

  path_matcher {
    name            = "allpaths"
    default_service = google_compute_backend_service.web_backend.id

    path_rule {
      paths   = ["/api/*"]
      service = google_compute_backend_service.api_backend.id
    }
  }
}

# 8.5 IP Estática Pública Global Reservada para el Load Balancer
resource "google_compute_global_address" "lb_ipv4" {
  name = "monchis-lb-ipv4"
}

# 8.6 Target HTTPS Proxy y Forwarding Rule (Puerto 443)
resource "google_compute_target_https_proxy" "https_proxy" {
  name             = "monchis-target-https-proxy"
  url_map          = google_compute_url_map.https_url_map.id
  ssl_certificates = [google_compute_managed_ssl_certificate.lb_ssl_cert.id]
}

resource "google_compute_global_forwarding_rule" "https_forwarding_rule" {
  name                  = "monchis-https-forwarding-rule"
  target                = google_compute_target_https_proxy.https_proxy.id
  port_range            = "443"
  ip_address            = google_compute_global_address.lb_ipv4.address
  load_balancing_scheme = "EXTERNAL_MANAGED"
}

# 8.7 Redirección Forzosa Global de HTTP (Puerto 80) a HTTPS (Puerto 443)
resource "google_compute_url_map" "http_redirect_map" {
  name = "monchis-http-redirect-map"
  default_url_redirect {
    https_redirect         = true
    redirect_response_code = "MOVED_PERMANENTLY_DEFAULT"
    strip_query            = false
  }
}

resource "google_compute_target_http_proxy" "http_proxy" {
  name    = "monchis-target-http-proxy"
  url_map = google_compute_url_map.http_redirect_map.id
}

resource "google_compute_global_forwarding_rule" "http_forwarding_rule" {
  name                  = "monchis-http-forwarding-rule"
  target                = google_compute_target_http_proxy.http_proxy.id
  port_range            = "80"
  ip_address            = google_compute_global_address.lb_ipv4.address
  load_balancing_scheme = "EXTERNAL_MANAGED"
}

