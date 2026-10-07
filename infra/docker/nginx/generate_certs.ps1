<#
.SYNOPSIS
    Monchis Café — Generador de Certificados SSL/TLS para Entorno Local / Staging en Windows
#>
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CertsDir = Join-Path $ScriptDir "certs"

if (-not (Test-Path $CertsDir)) {
    New-Item -ItemType Directory -Path $CertsDir | Out-Null
}

Write-Host "🔐 Generando certificados SSL/TLS autofirmados (RSA 4096-bit, SHA-256)..." -ForegroundColor Cyan

$KeyPath = Join-Path $CertsDir "key.pem"
$CertPath = Join-Path $CertsDir "cert.pem"

openssl req -x509 -newkey rsa:4096 -sha256 -days 365 -nodes `
    -keyout $KeyPath `
    -out $CertPath `
    -subj "/CN=localhost/O=Monchis Cafe/C=MX" `
    -addext "subjectAltName=DNS:localhost,DNS:monchiscafe.local,IP:127.0.0.1"

Write-Host "✅ Certificados generados exitosamente en: $CertsDir" -ForegroundColor Green
