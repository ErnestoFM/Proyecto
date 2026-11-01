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
      dosFactoresActivo: false,
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

  const p6 = await prisma.product.create({
    data: {
      nombre: 'Café de Olla Tradicional de Rancho',
      descripcion: 'Piloncillo de caña pura, canela en raja y clavo dulce en olla de barro',
      tipo: ProductType.ORGANICO,
      precio: 48.0,
      stockActual: 60,
      stockMinimo: 10,
      activo: true,
    },
  });

  const p7 = await prisma.product.create({
    data: {
      nombre: 'Latte Lavanda & Miel Silvestre',
      descripcion: 'Espresso balanceado con lavanda francesa orgánica y miel cruda de abeja',
      tipo: ProductType.ORGANICO,
      precio: 72.0,
      stockActual: 30,
      stockMinimo: 8,
      activo: true,
    },
  });

  const p8 = await prisma.product.create({
    data: {
      nombre: 'Mocha Artesanal Chocolate Tabasco 70%',
      descripcion: 'Doble shot con cacao criollo de Tabasco y leche cremada',
      tipo: ProductType.ORGANICO,
      precio: 78.0,
      stockActual: 35,
      stockMinimo: 8,
      activo: true,
    },
  });

  const p9 = await prisma.product.create({
    data: {
      nombre: 'Capuchino Clásico Tostado',
      descripcion: 'Espresso de altura, leche vaporizada y espuma aterciopelada con canela',
      tipo: ProductType.ORGANICO,
      precio: 58.0,
      stockActual: 45,
      stockMinimo: 10,
      activo: true,
    },
  });

  const p10 = await prisma.product.create({
    data: {
      nombre: 'Filtrado V60 Monorigen Pluma Hidalgo',
      descripcion: 'Extracción artesanal de goteo con notas florales y acidez cítrica brillante',
      tipo: ProductType.ORGANICO,
      precio: 80.0,
      stockActual: 25,
      stockMinimo: 5,
      activo: true,
    },
  });

  const p11 = await prisma.product.create({
    data: {
      nombre: 'Bolsa Café Chiapas Altura 250g',
      descripcion: 'Granos cosechados a 1,450 msnm bajo sombra natural, tueste medio artesanal',
      tipo: ProductType.ORGANICO,
      precio: 165.0,
      stockActual: 20,
      stockMinimo: 4,
      activo: true,
    },
  });

  const p12 = await prisma.product.create({
    data: {
      nombre: 'Bolsa Café Oaxaca Pluma Hidalgo 250g',
      descripcion: 'Lote selecto con notas a frutos secos, chocolate amargo y miel de abeja',
      tipo: ProductType.ORGANICO,
      precio: 185.0,
      stockActual: 18,
      stockMinimo: 4,
      activo: true,
    },
  });

  const p13 = await prisma.product.create({
    data: {
      nombre: 'Pan de Plátano Casero con Nuez',
      descripcion: 'Receta de rancho horneada diariamente con plátano maduro y nuez pecana',
      tipo: ProductType.COMERCIAL,
      precio: 48.0,
      stockActual: 24,
      stockMinimo: 6,
      activo: true,
    },
  });

  const p14 = await prisma.product.create({
    data: {
      nombre: 'Scone Rústico de Arándanos y Limón',
      descripcion: 'Panecillo tradicional horneado con arándanos silvestres y ralladura fresca',
      tipo: ProductType.COMERCIAL,
      precio: 42.0,
      stockActual: 20,
      stockMinimo: 5,
      activo: true,
    },
  });

  const p15 = await prisma.product.create({
    data: {
      nombre: 'Bagel Rústico Jamón Serrano y Rúcula',
      descripcion: 'Horneado a la leña con finas lascas de jamón serrano, queso crema y rúcula',
      tipo: ProductType.COMERCIAL,
      precio: 85.0,
      stockActual: 15,
      stockMinimo: 5,
      activo: true,
    },
  });

  const p16 = await prisma.product.create({
    data: {
      nombre: 'Galleta Suave de Avena, Cacao y Nuez',
      descripcion: 'Hojuelas de avena orgánica, chispas de cacao puro 70% y nuez troceada',
      tipo: ProductType.COMERCIAL,
      precio: 38.0,
      stockActual: 30,
      stockMinimo: 8,
      activo: true,
    },
  });

  console.log('☕ Catálogo de 16 productos creado con éxito.');

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
      createdAt: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000), // Hace 4 días
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

  const orden2 = await prisma.order.create({
    data: {
      total: 160.0,
      descuento: 0,
      metodoPago: PaymentMethod.TARJETA,
      estado: OrderStatus.COMPLETADA,
      clienteId: cliente.id,
      cajeroId: cajero.id,
      createdAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), // Hace 2 días
      items: {
        create: [
          { productoId: p2.id, cantidad: 1, precioUnitario: 75.0, subtotal: 75.0 },
          { productoId: p15.id, cantidad: 1, precioUnitario: 85.0, subtotal: 85.0 },
        ],
      },
      attributions: {
        create: {
          utmSource: 'instagram',
          utmMedium: 'social_profile',
          utmCampaign: 'historias_destacadas',
        },
      },
    },
  });

  const orden3 = await prisma.order.create({
    data: {
      total: 151.0,
      descuento: 0,
      metodoPago: PaymentMethod.TRANSFERENCIA,
      referenciaPago: 'SPEI-92384712',
      estado: OrderStatus.COMPLETADA,
      clienteId: cliente.id,
      cajeroId: cajero.id,
      createdAt: new Date(Date.now() - 3 * 60 * 60 * 1000), // Hace 3 horas
      items: {
        create: [
          { productoId: p6.id, cantidad: 1, precioUnitario: 48.0, subtotal: 48.0 },
          { productoId: p13.id, cantidad: 1, precioUnitario: 48.0, subtotal: 48.0 },
          { productoId: p5.id, cantidad: 1, precioUnitario: 55.0, subtotal: 55.0 },
        ],
      },
      attributions: {
        create: {
          utmSource: 'direct_visit',
          utmMedium: 'walk_in',
          utmCampaign: 'mostrador',
        },
      },
    },
  });

  console.log(`🧾 3 Órdenes de muestra creadas para analítica e historial: ${orden1.id}, ${orden2.id}, ${orden3.id}`);
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
