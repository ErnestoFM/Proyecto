output "web_service_url" {
  description = "URL pública de la aplicación frontend Monchis Café en Cloud Run"
  value       = google_cloud_run_v2_service.web_service.uri
}

output "api_service_url" {
  description = "URL pública del backend API Gateway en Cloud Run"
  value       = google_cloud_run_v2_service.api_service.uri
}

output "postgres_public_ip" {
  description = "Dirección IP pública de la base de datos PostgreSQL en Cloud SQL"
  value       = google_sql_database_instance.postgres_instance.public_ip_address
}

output "redis_host" {
  description = "Host del clúster de Cloud Memorystore Redis"
  value       = google_redis_instance.cache.host
}
