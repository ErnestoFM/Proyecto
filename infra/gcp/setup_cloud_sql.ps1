<#
.SYNOPSIS
    Script de aprovisionamiento automatizado para Google Cloud SQL (PostgreSQL 15) en Monchis Café.
.DESCRIPTION
    Crea la instancia en Google Cloud Platform, la base de datos monchis_db,
    el usuario administrador, y configura el string de conexión para Prisma ORM.
#>

param (
    [string]$ProjectId = "leadforge-499919",
    [string]$Region = "us-central1",
    [string]$InstanceName = "monchis-cafe-postgres-prod",
    [string]$DbName = "monchis_db",
    [string]$DbUser = "monchis_admin",
    [string]$DbPassword = "MonchisSecure2026!DB",
    [string]$Tier = "db-f1-micro"
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Monchis Café — Aprovisionamiento de Google Cloud SQL    " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Verificar autenticación activa de gcloud
Write-Host "`n[1/5] Verificando cuenta activa en Google Cloud..." -ForegroundColor Yellow
$currentAccount = gcloud config get-value account 2>$null
if (-not $currentAccount) {
    Write-Error "No hay cuenta activa en gcloud. Ejecuta: gcloud auth login"
    exit 1
}
Write-Host "Cuenta autenticada: $currentAccount" -ForegroundColor Green

# 2. Establecer proyecto de GCP
Write-Host "`n[2/5] Configurando proyecto objetivo: $ProjectId..." -ForegroundColor Yellow
gcloud config set project $ProjectId

# Habilitar API de Cloud SQL si no está activa
Write-Host "Habilitando servicio sqladmin.googleapis.com..." -ForegroundColor Yellow
gcloud services enable sqladmin.googleapis.com --project=$ProjectId

# 3. Crear Instancia de Cloud SQL (PostgreSQL 15)
Write-Host "`n[3/5] Verificando / Creando instancia Cloud SQL: $InstanceName..." -ForegroundColor Yellow
$instanceExists = gcloud sql instances list --filter="name:$InstanceName" --format="value(name)" 2>$null

if (-not $instanceExists) {
    Write-Host "Creando instancia $InstanceName (Tier: $Tier, Región: $Region)..." -ForegroundColor Yellow
    gcloud sql instances create $InstanceName `
        --database-version=POSTGRES_15 `
        --tier=$Tier `
        --region=$Region `
        --storage-type=SSD `
        --storage-size=10GB `
        --backup `
        --retained-backups-count=7 `
        --project=$ProjectId
    Write-Host "Instancia creada con éxito." -ForegroundColor Green
} else {
    Write-Host "La instancia $InstanceName ya existe. Omitiendo creación." -ForegroundColor Green
}

# 4. Crear Base de Datos y Usuario
Write-Host "`n[4/5] Creando base de datos $DbName y usuario $DbUser..." -ForegroundColor Yellow
gcloud sql databases create $DbName --instance=$InstanceName --project=$ProjectId 2>$null
gcloud sql users create $DbUser --instance=$InstanceName --password=$DbPassword --project=$ProjectId 2>$null

# Obtener IP Pública de la instancia
$publicIp = gcloud sql instances describe $InstanceName --format="value(ipAddresses[0].ipAddress)" --project=$ProjectId

Write-Host "`n[5/5] Resumen de Conexión a Google Cloud SQL:" -ForegroundColor Cyan
Write-Host "  Instancia: $InstanceName" -ForegroundColor White
Write-Host "  IP Pública: $publicIp" -ForegroundColor White
Write-Host "  Base de Datos: $DbName" -ForegroundColor White
Write-Host "  Usuario: $DbUser" -ForegroundColor White

$connectionString = "postgresql://${DbUser}:${DbPassword}@${publicIp}:5432/${DbName}?schema=public"
Write-Host "`nDATABASE_URL generado para .env y Prisma:" -ForegroundColor Yellow
Write-Host $connectionString -ForegroundColor Green

Write-Host "`nPara sincronizar el esquema y los datos iniciales, ejecuta:" -ForegroundColor Cyan
Write-Host "  `$env:DATABASE_URL = `"$connectionString`""
Write-Host "  pnpm prisma:migrate"
Write-Host "  pnpm --filter @monchis/database seed"
Write-Host "`n¡Aprovisionamiento finalizado con éxito!" -ForegroundColor Green
