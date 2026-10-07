#!/usr/bin/env bash
# ==============================================================================
# Monchis Café — Generador de Certificados SSL/TLS para Entorno Local / Staging
# ==============================================================================
set -e

CERTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/certs" && pwd)"
mkdir -p "$CERTS_DIR"

echo "🔐 Generando certificados SSL/TLS autofirmados (RSA 4096-bit, SHA-256)..."

openssl req -x509 -newkey rsa:4096 -sha256 -days 365 -nodes \
  -keyout "$CERTS_DIR/key.pem" \
  -out "$CERTS_DIR/cert.pem" \
  -subj "/CN=localhost/O=Monchis Cafe/C=MX" \
  -addext "subjectAltName=DNS:localhost,DNS:monchiscafe.local,IP:127.0.0.1"

chmod 600 "$CERTS_DIR/key.pem"
chmod 644 "$CERTS_DIR/cert.pem"

echo "✅ Certificados generados exitosamente en: $CERTS_DIR"
