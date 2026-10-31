variable "project_id" {
  description = "Google Cloud Project ID (Obligatorio, definir en .tfvars o TF_VAR_project_id)"
  type        = string
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
  description = "Contraseña para la instancia de PostgreSQL en Cloud SQL (Obligatorio, sensible)"
  type        = string
  sensitive   = true
}

variable "jwt_access_secret" {
  description = "Llave secreta para emisión de JWT Access Tokens (mínimo 32 caracteres)"
  type        = string
  sensitive   = true
}

variable "jwt_refresh_secret" {
  description = "Llave secreta para emisión de JWT Refresh Tokens (mínimo 32 caracteres)"
  type        = string
  sensitive   = true
}

variable "recaptcha_secret_key" {
  description = "Google reCAPTCHA Secret Key"
  type        = string
  sensitive   = true
}

variable "domain_name" {
  description = "Dominio principal de producción para certificados SSL (ej. monchiscafe.com)"
  type        = string
  default     = "monchiscafe.com"
}

