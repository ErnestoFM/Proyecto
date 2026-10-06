# Monchis Café — Guía de Infraestructura en Google Cloud SQL (PostgreSQL)

Esta guía detalla la configuración y despliegue del motor de persistencia relacional utilizando el servicio gestionado **Google Cloud SQL para PostgreSQL 15**.

---

## 1. Opciones de Conectividad

| Escenario | Método Recomendado | Descripción |
|---|---|---|
| **Desarrollo Local** | **Cloud SQL Auth Proxy** | Comunicación cifrada por TLS mediante credenciales IAM (`gcloud auth`), sin necesidad de abrir la IP pública a internet. |
| **Desarrollo Alterno** | **IP Pública Autorizada** | Se agrega la IP pública del desarrollador en `Authorized Networks` de la instancia de Cloud SQL. |
| **Producción (Cloud Run)** | **Unix Sockets / Cloud SQL Connector** | Cloud Run se conecta nativamente mediante `/cloudsql/INSTANCE_CONNECTION_NAME` con costo de red cero interno. |

---

## 2. Aprovisionamiento Automatizado

Ejecuta el script PowerShell incluido en `infra/gcp/setup_cloud_sql.ps1`:

```powershell
# Dentro de la raíz del proyecto
.\infra\gcp\setup_cloud_sql.ps1 -ProjectId "leadforge-499919" -Region "us-central1" -DbPassword "TuContraseñaSegura2026!"
```

---

## 3. Conexión Local con Cloud SQL Auth Proxy (Recomendado)

1. Descarga el ejecutable oficial `cloud-sql-proxy.exe` de Google Cloud.
2. Inicia el proxy en el puerto local 5432:
   ```bash
   cloud-sql-proxy PROJECT_ID:REGION:monchis-cafe-postgres-prod --port 5432
   ```
3. Configura tu `.env`:
   ```env
   DATABASE_URL="postgresql://monchis_admin:TuContraseñaSegura2026!@localhost:5432/monchis_db?schema=public"
   ```
4. Ejecuta las migraciones y el seeder inicial:
   ```bash
   pnpm prisma:migrate
   pnpm --filter @monchis/database seed
   ```

---

## 4. Conexión Alterna vía IP Pública Directa

Si prefieres conectar directamente sin proxy:
1. Agrega tu IP pública actual:
   ```bash
   gcloud sql instances patch monchis-cafe-postgres-prod --authorized-networks=TU_IP_PUBLICA/32
   ```
2. Obtén la IP pública de la instancia:
   ```bash
   gcloud sql instances describe monchis-cafe-postgres-prod --format="value(ipAddresses[0].ipAddress)"
   ```
3. Configura tu `.env`:
   ```env
   DATABASE_URL="postgresql://monchis_admin:TuContraseñaSegura2026!@IP_PUBLICA_CLOUDSQL:5432/monchis_db?schema=public"
   ```
