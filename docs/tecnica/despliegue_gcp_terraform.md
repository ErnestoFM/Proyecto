# Guía de Despliegue en Google Cloud Platform (IaC con Terraform) — Monchis Café

Este documento describe el procedimiento paso a paso para el aprovisionamiento de infraestructura y despliegue automatizado de **Monchis Café** en Google Cloud Platform.

---

## ☁️ 1. Arquitectura Desplegada

| Componente | Servicio GCP | Función |
|---|---|---|
| **Frontend Web** | Google Cloud Run (v2) | Alojamiento serverless de la SPA prerenderizada Vue 3 + `vite-ssg`. |
| **Backend API** | Google Cloud Run (v2) | API Gateway y microservicios Next.js (Auth, POS, Inventory, Admin). |
| **Base de Datos** | Google Cloud SQL (PostgreSQL 15) | Persistencia relacional de usuarios, lotes de café, órdenes y transacciones. |
| **Caché & Rate-Limit** | Google Cloud Memorystore (Redis 7) | Almacenamiento volátil para mitigación de ataques y rate limiting. |
| **Secretos** | Google Secret Manager | Llaves criptográficas de JWT, Secret Key de Google reCAPTCHA y credenciales de DB. |
| **Seguridad WAF** | Google Cloud Armor | Políticas anti-DDoS y mitigación de fuerza bruta (bloqueo automático a >120 req/min por IP). |

---

## 🚀 2. Comandos de Inicialización y Despliegue

### Paso 1: Autenticación con Google Cloud SDK
```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project gen-lang-client-0573629438
```

### Paso 2: Habilitar APIs Necesarias en GCP
```bash
gcloud services enable \
  run.googleapis.com \
  sqladmin.googleapis.com \
  redis.googleapis.com \
  secretmanager.googleapis.com \
  compute.googleapis.com \
  cloudbuild.googleapis.com
```

### Paso 3: Planificación y Aplicación con Terraform
```bash
cd infra/terraform
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

### Paso 4: Despliegue de Contenedores con Cloud Build
```bash
# Construir y publicar imágenes
gcloud builds submit --tag gcr.io/gen-lang-client-0573629438/monchis-api:latest -f infra/docker/auth-service/Dockerfile .
gcloud builds submit --tag gcr.io/gen-lang-client-0573629438/monchis-web:latest -f infra/docker/api-gateway/Dockerfile .
```
