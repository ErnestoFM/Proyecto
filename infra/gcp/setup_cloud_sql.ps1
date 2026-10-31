<#
.SYNOPSIS
    Script de aprovisionamiento automatizado para Google Cloud SQL (PostgreSQL 15) en Monchis Café.
.DESCRIPTION
    Crea la instancia en Google Cloud Platform, la base de datos monchis_db,
    el usuario administrador, y configura el string de conexión en Google Secret Manager para Prisma ORM.
#>

param (
    [string]$ProjectId = $(if ($env:GCP_PROJECT_ID) { $env:GCP_PROJECT_ID } else { (gcloud config get-value project 2>$null) }),
    [string]$Region = $(if ($env:GCP_REGION) { $env:GCP_REGION } else { "us-central1" }),
    [string]$InstanceName = "monchis-cafe-postgres-prod",
    [string]$DbName = "monchis_db",
    [string]$DbUser = "monchis_admin",
    [string]$DbPassword = $(if ($env:DB_PASSWORD) { $env:DB_PASSWORD } else { -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 28 | ForEach-Object {[char]$_}) }),
    [string]$Tier = "db-f1-micro",
    [string]$AuthorizedNetwork = ""
)

if (-not $ProjectId) {
    Write-Error "[Seguridad] ProjectId es obligatorio. Configura `$env:GCP_PROJECT_ID o gcloud config set project <ID>."
    exit 1
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Monchis Café — Aprovisionamiento de Google Cloud SQL    " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Configurar proyecto de GCP
Write-Host "`n[1/5] Configurando proyecto objetivo: $ProjectId..." -ForegroundColor Yellow
gcloud config set project $ProjectId

# 2. Habilitar servicios
Write-Host "`n[2/5] Habilitando servicios necesarios (sqladmin, secretmanager)..." -ForegroundColor Yellow
gcloud services enable sqladmin.googleapis.com secretmanager.googleapis.com --project=$ProjectId

# 3. Crear Instancia de Cloud SQL
Write-Host "`n[3/5] Verificando / Creando instancia Cloud SQL: $InstanceName..." -ForegroundColor Yellow
$instanceExists = gcloud sql instances list --filter="name:$InstanceName" --format="value(name)" --project=$ProjectId 2>$null

if (-not $instanceExists) {
    Write-Host "Creando instancia $InstanceName (Tier: $Tier, Región: $Region)..." -ForegroundColor Yellow
    $createArgs = @(
        "sql", "instances", "create", $InstanceName,
        "--database-version=POSTGRES_15",
        "--tier=$Tier",
        "--region=$Region",
        "--storage-type=SSD",
        "--storage-size=10GB",
        "--backup",
        "--retained-backups-count=7",
        "--project=$ProjectId"
    )
    if ($AuthorizedNetwork) {
        $createArgs += "--authorized-networks=$AuthorizedNetwork"
    }
    gcloud @createArgs
    Write-Host "Instancia creada con éxito." -ForegroundColor Green
} else {
    Write-Host "La instancia $InstanceName ya existe. Omitiendo creación." -ForegroundColor Green
}

# 4. Crear Base de Datos y Usuario
Write-Host "`n[4/5] Creando base de datos $DbName y usuario $DbUser..." -ForegroundColor Yellow
gcloud sql databases create $DbName --instance=$InstanceName --project=$ProjectId 2>$null
gcloud sql users create $DbUser --instance=$InstanceName --password=$DbPassword --project=$ProjectId 2>$null

# 5. Obtener IP Pública de la instancia
$publicIp = gcloud sql instances describe $InstanceName --format="value(ipAddresses[0].ipAddress)" --project=$ProjectId

Write-Host "`n[5/5] Resumen de Conexión a Google Cloud SQL:" -ForegroundColor Cyan
Write-Host "  Instancia: $InstanceName" -ForegroundColor White
Write-Host "  IP Pública: $publicIp" -ForegroundColor White
Write-Host "  Base de Datos: $DbName" -ForegroundColor White
Write-Host "  Usuario: $DbUser" -ForegroundColor White

$connectionString = "postgresql://${DbUser}:${DbPassword}@${publicIp}:5432/${DbName}?sslmode=prefer"
Write-Host "`nDATABASE_URL generado:" -ForegroundColor Yellow
Write-Host "postgresql://${DbUser}:********@${publicIp}:5432/${DbName}" -ForegroundColor Green

# Guardar en Secret Manager
Write-Host "`nGuardando DATABASE_URL en Google Secret Manager (monchis-database-url)..." -ForegroundColor Yellow
$connectionString | gcloud secrets create monchis-database-url --data-file=- --project=$ProjectId 2>$null
if ($LASTEXITCODE -ne 0) {
    $connectionString | gcloud secrets versions add monchis-database-url --data-file=- --project=$ProjectId 2>$null
}

Write-Host "`n¡Aprovisionamiento finalizado con éxito!" -ForegroundColor Green
