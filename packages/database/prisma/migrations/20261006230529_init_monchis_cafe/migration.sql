-- CreateEnum
CREATE TYPE "Role" AS ENUM ('ADMIN', 'CAJERO', 'CLIENTE');

-- CreateEnum
CREATE TYPE "ProductType" AS ENUM ('ORGANICO', 'COMERCIAL');

-- CreateEnum
CREATE TYPE "PaymentMethod" AS ENUM ('EFECTIVO', 'TARJETA', 'TRANSFERENCIA', 'PUNTOS', 'MIXTO');

-- CreateEnum
CREATE TYPE "OrderStatus" AS ENUM ('PENDIENTE', 'PROCESANDO', 'COMPLETADA', 'CANCELADA_REEMBOLSADA');

-- CreateTable
CREATE TABLE "User" (
    "id" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "passwordHash" TEXT NOT NULL,
    "nombre" TEXT NOT NULL,
    "rol" "Role" NOT NULL DEFAULT 'CLIENTE',
    "dosFactoresActivo" BOOLEAN NOT NULL DEFAULT false,
    "dosFactoresSecret" TEXT,
    "puntosFidelidad" INTEGER NOT NULL DEFAULT 0,
    "sellosAcumulados" INTEGER NOT NULL DEFAULT 0,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "RevokedToken" (
    "id" TEXT NOT NULL,
    "tokenJti" TEXT NOT NULL,
    "expiraEn" TIMESTAMP(3) NOT NULL,
    "motivo" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "RevokedToken_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Product" (
    "id" TEXT NOT NULL,
    "nombre" TEXT NOT NULL,
    "descripcion" TEXT,
    "tipo" "ProductType" NOT NULL DEFAULT 'ORGANICO',
    "precio" DECIMAL(10,2) NOT NULL,
    "stockActual" INTEGER NOT NULL DEFAULT 0,
    "stockMinimo" INTEGER NOT NULL DEFAULT 5,
    "imagenUrl" TEXT,
    "activo" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Product_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Batch" (
    "id" TEXT NOT NULL,
    "productoId" TEXT NOT NULL,
    "numeroLote" TEXT NOT NULL,
    "proveedorRegional" TEXT NOT NULL,
    "fincaOrigen" TEXT,
    "fechaCosechaTostado" TIMESTAMP(3) NOT NULL,
    "fechaCaducidad" TIMESTAMP(3) NOT NULL,
    "cantidadKilos" DECIMAL(10,2) NOT NULL,
    "alertasSanitarias" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Batch_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Order" (
    "id" TEXT NOT NULL,
    "total" DECIMAL(10,2) NOT NULL,
    "descuento" DECIMAL(10,2) NOT NULL DEFAULT 0,
    "metodoPago" "PaymentMethod" NOT NULL DEFAULT 'EFECTIVO',
    "referenciaPago" TEXT,
    "estado" "OrderStatus" NOT NULL DEFAULT 'PROCESANDO',
    "clienteId" TEXT,
    "cajeroId" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Order_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "OrderItem" (
    "id" TEXT NOT NULL,
    "orderId" TEXT NOT NULL,
    "productoId" TEXT NOT NULL,
    "cantidad" INTEGER NOT NULL,
    "precioUnitario" DECIMAL(10,2) NOT NULL,
    "subtotal" DECIMAL(10,2) NOT NULL,

    CONSTRAINT "OrderItem_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Attribution" (
    "id" TEXT NOT NULL,
    "orderId" TEXT,
    "userId" TEXT,
    "utmSource" TEXT NOT NULL,
    "utmMedium" TEXT,
    "utmCampaign" TEXT,
    "ipAddress" TEXT,
    "userAgent" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Attribution_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "SagaStateLog" (
    "id" TEXT NOT NULL,
    "sagaId" TEXT NOT NULL,
    "orderId" TEXT NOT NULL,
    "estadoActual" "OrderStatus" NOT NULL,
    "eventosEjecutados" JSONB NOT NULL DEFAULT '[]',
    "compensacionesEjecutadas" JSONB NOT NULL DEFAULT '[]',
    "motivoFalla" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "SagaStateLog_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");

-- CreateIndex
CREATE INDEX "User_email_idx" ON "User"("email");

-- CreateIndex
CREATE INDEX "User_rol_idx" ON "User"("rol");

-- CreateIndex
CREATE UNIQUE INDEX "RevokedToken_tokenJti_key" ON "RevokedToken"("tokenJti");

-- CreateIndex
CREATE INDEX "RevokedToken_tokenJti_idx" ON "RevokedToken"("tokenJti");

-- CreateIndex
CREATE INDEX "Product_tipo_idx" ON "Product"("tipo");

-- CreateIndex
CREATE INDEX "Product_activo_idx" ON "Product"("activo");

-- CreateIndex
CREATE UNIQUE INDEX "Batch_numeroLote_key" ON "Batch"("numeroLote");

-- CreateIndex
CREATE INDEX "Batch_productoId_idx" ON "Batch"("productoId");

-- CreateIndex
CREATE INDEX "Batch_numeroLote_idx" ON "Batch"("numeroLote");

-- CreateIndex
CREATE INDEX "Batch_fechaCaducidad_idx" ON "Batch"("fechaCaducidad");

-- CreateIndex
CREATE INDEX "Order_estado_idx" ON "Order"("estado");

-- CreateIndex
CREATE INDEX "Order_clienteId_idx" ON "Order"("clienteId");

-- CreateIndex
CREATE INDEX "Order_cajeroId_idx" ON "Order"("cajeroId");

-- CreateIndex
CREATE INDEX "Order_createdAt_idx" ON "Order"("createdAt");

-- CreateIndex
CREATE INDEX "OrderItem_orderId_idx" ON "OrderItem"("orderId");

-- CreateIndex
CREATE INDEX "OrderItem_productoId_idx" ON "OrderItem"("productoId");

-- CreateIndex
CREATE INDEX "Attribution_utmSource_idx" ON "Attribution"("utmSource");

-- CreateIndex
CREATE INDEX "Attribution_createdAt_idx" ON "Attribution"("createdAt");

-- CreateIndex
CREATE UNIQUE INDEX "SagaStateLog_sagaId_key" ON "SagaStateLog"("sagaId");

-- CreateIndex
CREATE INDEX "SagaStateLog_sagaId_idx" ON "SagaStateLog"("sagaId");

-- CreateIndex
CREATE INDEX "SagaStateLog_orderId_idx" ON "SagaStateLog"("orderId");

-- AddForeignKey
ALTER TABLE "Batch" ADD CONSTRAINT "Batch_productoId_fkey" FOREIGN KEY ("productoId") REFERENCES "Product"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Order" ADD CONSTRAINT "Order_clienteId_fkey" FOREIGN KEY ("clienteId") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Order" ADD CONSTRAINT "Order_cajeroId_fkey" FOREIGN KEY ("cajeroId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "OrderItem" ADD CONSTRAINT "OrderItem_orderId_fkey" FOREIGN KEY ("orderId") REFERENCES "Order"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "OrderItem" ADD CONSTRAINT "OrderItem_productoId_fkey" FOREIGN KEY ("productoId") REFERENCES "Product"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Attribution" ADD CONSTRAINT "Attribution_orderId_fkey" FOREIGN KEY ("orderId") REFERENCES "Order"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Attribution" ADD CONSTRAINT "Attribution_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "SagaStateLog" ADD CONSTRAINT "SagaStateLog_orderId_fkey" FOREIGN KEY ("orderId") REFERENCES "Order"("id") ON DELETE CASCADE ON UPDATE CASCADE;
