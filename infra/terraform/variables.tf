variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
  default     = "gen-lang-client-0573629438"
}

variable "region" {
  description = "Región principal de GCP para el despliegue"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Entorno de despliegue (dev, staging, prod)"
  type        = string
  default     = "prod"
}

variable "db_password" {
  description = "Contraseña para la instancia de PostgreSQL en Cloud SQL"
  type        = string
  sensitive   = true
  default     = "MonchisSecure2026!DB"
}

variable "jwt_access_secret" {
  description = "Llave secreta para emisión de JWT Access Tokens"
  type        = string
  sensitive   = true
  default     = "monchis-cafe-access-secret-32-chars-min"
}

variable "jwt_refresh_secret" {
  description = "Llave secreta para emisión de JWT Refresh Tokens"
  type        = string
  sensitive   = true
  default     = "monchis-cafe-refresh-secret-32-chars-min"
}

variable "recaptcha_secret_key" {
  description = "Google reCAPTCHA Secret Key"
  type        = string
  sensitive   = true
  default     = "mock-google-recaptcha-secret-key"
}
