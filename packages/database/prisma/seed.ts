import { PrismaClient, Role, ProductType, PaymentMethod, OrderStatus } from '@prisma/client';
import * as bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Iniciando carga de datos semilla (Seed) para Monchis Café...');

  // 1. Limpieza controlada en orden de relaciones
  await prisma.attribution.deleteMany();
  await prisma.sagaStateLog.deleteMany();
  await prisma.orderItem.deleteMany();
  await prisma.order.deleteMany();
  await prisma.batch.deleteMany();
  await prisma.product.deleteMany();
  await prisma.revokedToken.deleteMany();
  await prisma.user.deleteMany();

  console.log('🧹 Tablas limpiadas.');

  // 2. Usuarios Base
  const salt = await bcrypt.genSalt(10);
  const passwordHashAdmin = await bcrypt.hash('Admin123!*', salt);
  const passwordHashCajero = await bcrypt.hash('Cajero123!*', salt);
  const passwordHashCliente = await bcrypt.hash('Cliente123!*', salt);

  const admin = await prisma.user.create({
    data: {
      email: 'admin@monchiscafe.com',
      passwordHash: passwordHashAdmin,
      nombre: 'Administrador Monchis',
      rol: Role.ADMIN,
      dosFactoresActivo: true,
      puntosFidelidad: 0,
      sellosAcumulados: 0,
    },
  });

  const cajero = await prisma.user.create({
    data: {
      email: 'cajero@monchiscafe.com',
      passwordHash: passwordHashCajero,
      nombre: 'Cajero Mostrador 1',
      rol: Role.CAJERO,
      dosFactoresActivo: false,
      puntosFidelidad: 0,
      sellosAcumulados: 0,
    },
  });

  const cliente = await prisma.user.create({
    data: {
      email: 'cliente@monchiscafe.com',
      passwordHash: passwordHashCliente,
      nombre: 'Ernesto Fierro (Cliente Leal)',
      rol: Role.CLIENTE,
      dosFactoresActivo: false,
      puntosFidelidad: 120,
      sellosAcumulados: 4,
    },
  });

  console.log(`👤 Usuarios creados: Admin (${admin.email}), Cajero (${cajero.email}), Cliente (${cliente.email})`);

  // 3. Catálogo de Productos
  const p1 = await prisma.product.create({
    data: {
      nombre: 'Café Americano Chiapas Orgánico',
      descripcion: 'Notas a cacao y frutos secos, tostado medio artesanal',
      tipo: ProductType.ORGANICO,
      precio: 65.0,
      stockActual: 50,
      stockMinimo: 10,
      activo: true,
    },
  });

  const p2 = await prisma.product.create({
    data: {
      nombre: 'Cold Brew Macerado 18h Orgánico',
      descripcion: 'Extracción en frío con granos orgánicos de altura',
      tipo: ProductType.ORGANICO,
      precio: 75.0,
      stockActual: 35,
      stockMinimo: 8,
      activo: true,
    },
  });

  const p3 = await prisma.product.create({
    data: {
      nombre: 'Espresso Doble Comercial',
      descripcion: 'Mezcla comercial italiana con cuerpo denso y crema intensa',
      tipo: ProductType.COMERCIAL,
      precio: 45.0,
      stockActual: 70,
      stockMinimo: 15,
      activo: true,
    },
  });

  const p4 = await prisma.product.create({
    data: {
      nombre: 'Flat White Artesanal Orgánico',
      descripcion: 'Doble ristretto con leche cremada microespumada',
      tipo: ProductType.ORGANICO,
      precio: 70.0,
      stockActual: 40,
      stockMinimo: 10,
      activo: true,
    },
  });

  const p5 = await prisma.product.create({
    data: {
      nombre: 'Croissant Horneado con Mantequilla',
      descripcion: 'Bollería artesanal del día',
      tipo: ProductType.COMERCIAL,
      precio: 55.0,
      stockActual: 20,
      stockMinimo: 5,
      activo: true,
    },
  });

  console.log('☕ Catálogo de 5 productos creado.');

  // 4. Lotes de Origen con Trazabilidad Sanitaria
  const lote1 = await prisma.batch.create({
    data: {
      productoId: p1.id,
      numeroLote: 'LOTE-2026-CH-01',
      proveedorRegional: 'Cooperativa Maya Vinic',
      fincaOrigen: 'Finca Santa Anita, Simojovel, Chiapas (1,450 msnm)',
      fechaCosechaTostado: new Date('2026-08-10'),
      fechaCaducidad: new Date('2027-02-10'),
      cantidadKilos: 25.5,
      alertasSanitarias: 'Certificación Orgánica SAGARPA / CERTIMEX vigente.',
    },
  });

  const lote2 = await prisma.batch.create({
    data: {
      productoId: p2.id,
      numeroLote: 'LOTE-2026-VR-02',
      proveedorRegional: 'Cafetaleros de Coatepec',
      fincaOrigen: 'Finca Las Nubes, Coatepec, Veracruz (1,250 msnm)',
      fechaCosechaTostado: new Date('2026-08-20'),
      fechaCaducidad: new Date('2027-02-20'),
      cantidadKilos: 30.0,
      alertasSanitarias: 'Inspección fitosanitaria libre de broca y humedad.',
    },
  });

  console.log(`📦 Lotes de trazabilidad creados: ${lote1.numeroLote}, ${lote2.numeroLote}`);

  // 5. Órdenes Históricas para Analítica
  const orden1 = await prisma.order.create({
    data: {
      total: 135.0,
      descuento: 0,
      metodoPago: PaymentMethod.EFECTIVO,
      estado: OrderStatus.COMPLETADA,
      clienteId: cliente.id,
      cajeroId: cajero.id,
      items: {
        create: [
          { productoId: p1.id, cantidad: 1, precioUnitario: 65.0, subtotal: 65.0 },
          { productoId: p4.id, cantidad: 1, precioUnitario: 70.0, subtotal: 70.0 },
        ],
      },
      attributions: {
        create: {
          utmSource: 'google_maps',
          utmMedium: 'organic_search',
          utmCampaign: 'local_pack',
        },
      },
    },
  });

  console.log(`🧾 Orden de muestra creada: ID ${orden1.id}`);
  console.log('✅ Seed completado exitosamente.');
}

main()
  .catch((e) => {
    console.error('❌ Error en seeder:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
