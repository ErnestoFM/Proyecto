// ==============================================================================
// Monchis Café — Servicio de Notificaciones por Correo SMTP (apps/api/src/lib/emailService.ts)
// Basado en Requerimientos Funcionales 2.2 (Caducidad) y 2.3 (Alerta DLQ)
// ==============================================================================

import nodemailer from 'nodemailer';
import type { Transporter } from 'nodemailer';

export interface DLQAlertPayload {
  orderId: string;
  motivo: string;
  intentos: number;
  sagaId?: string;
  timestamp?: string;
  detallesExtra?: Record<string, any>;
}

export interface BatchExpiryAlertPayload {
  numeroLote: string;
  productoNombre: string;
  fincaOrigen?: string;
  fechaCaducidad: string;
  diasRestantes: number;
}

export interface LowStockAlertPayload {
  productoId: string;
  productoNombre: string;
  stockActual: number;
  stockMinimo: number;
  tipo?: string;
}

export interface OrderReceiptPayload {
  clienteEmail: string;
  ordenId: string;
  total: number;
  metodoPago: string;
  items: Array<{
    nombre: string;
    cantidad: number;
    subtotal: number;
  }>;
  puntosGanados?: number;
  sellosAcumulados?: number;
}

export interface EmailSendResult {
  success: boolean;
  messageId?: string;
  error?: string;
  previewUrl?: string | false;
}

// Registro en memoria de correos emitidos en entorno de prueba o desarrollo
const EMAILS_SENT_LOG: Array<{
  to: string;
  subject: string;
  html: string;
  timestamp: string;
}> = [];

export function getSentEmailsLogForTesting() {
  return [...EMAILS_SENT_LOG];
}

export function clearSentEmailsLogForTesting() {
  EMAILS_SENT_LOG.length = 0;
}

export class EmailService {
  private static transporterInstance: Transporter | null = null;

  private static getTransporter(): Transporter {
    if (this.transporterInstance) {
      return this.transporterInstance;
    }

    const host = process.env.SMTP_HOST;
    const port = parseInt(process.env.SMTP_PORT || '587', 10);
    const user = process.env.SMTP_USER;
    const pass = process.env.SMTP_PASS;

    // Si no hay credenciales completas o estamos en testing, usamos JSON transport resiliente
    if (process.env.NODE_ENV === 'test' || !host || !user || !pass || pass.trim() === '') {
      this.transporterInstance = nodemailer.createTransport({
        jsonTransport: true,
      });
      return this.transporterInstance;
    }

    this.transporterInstance = nodemailer.createTransport({
      host,
      port,
      secure: port === 465,
      auth: {
        user,
        pass,
      },
    });

    return this.transporterInstance;
  }

  private static getAdminRecipient(): string {
    return process.env.ADMIN_ALERT_EMAIL || process.env.ADMIN_DEFAULT_EMAIL || 'admin@monchiscafe.com';
  }

  private static getFromAddress(): string {
    return process.env.SMTP_FROM || '"Monchis Café" <notificaciones@monchiscafe.com>';
  }

  /**
   * Alerta Crítica al Administrador por mensaje caído en Dead Letter Queue (Req 2.3)
   */
  public static async sendDLQAlert(payload: DLQAlertPayload): Promise<EmailSendResult> {
    const adminEmail = this.getAdminRecipient();
    const subject = `🚨 [ALERTA CRÍTICA DLQ] Mensaje en Dead Letter Queue - Orden #${payload.orderId}`;
    const fecha = payload.timestamp || new Date().toISOString();

    const html = `
      <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #fee2e2; border-radius: 8px; overflow: hidden;">
        <div style="background-color: #ef4444; color: white; padding: 20px; text-align: center;">
          <h2 style="margin: 0; font-size: 20px;">🚨 Alerta de Dead Letter Queue (DLQ)</h2>
          <p style="margin: 5px 0 0; font-size: 14px; opacity: 0.9;">Monchis Café — Sistema de Resiliencia y Fallos Saga</p>
        </div>
        <div style="padding: 24px; background-color: #ffffff; color: #1f2937;">
          <p style="font-size: 15px; line-height: 1.5;">Se ha registrado un evento fallido que superó el umbral de reintentos progresivos (10s, 60s, 300s) y ha sido desviado a la <strong>Dead Letter Queue</strong> para intervención manual.</p>
          
          <table style="width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px;">
            <tr style="border-bottom: 1px solid #f3f4f6;">
              <td style="padding: 8px; font-weight: bold; color: #4b5563;">Orden Afectada:</td>
              <td style="padding: 8px; font-family: monospace; color: #111827;">#${payload.orderId}</td>
            </tr>
            <tr style="border-bottom: 1px solid #f3f4f6;">
              <td style="padding: 8px; font-weight: bold; color: #4b5563;">Reintentos Ejecutados:</td>
              <td style="padding: 8px; color: #dc2626; font-weight: bold;">${payload.intentos} intentos</td>
            </tr>
            <tr style="border-bottom: 1px solid #f3f4f6;">
              <td style="padding: 8px; font-weight: bold; color: #4b5563;">Motivo del Fallo:</td>
              <td style="padding: 8px; color: #374151;">${payload.motivo}</td>
            </tr>
            ${payload.sagaId ? `
            <tr style="border-bottom: 1px solid #f3f4f6;">
              <td style="padding: 8px; font-weight: bold; color: #4b5563;">Saga ID:</td>
              <td style="padding: 8px; font-family: monospace;">${payload.sagaId}</td>
            </tr>` : ''}
            <tr>
              <td style="padding: 8px; font-weight: bold; color: #4b5563;">Marca de Tiempo:</td>
              <td style="padding: 8px; color: #6b7280;">${fecha}</td>
            </tr>
          </table>

          <div style="background-color: #fef2f2; border-left: 4px solid #ef4444; padding: 12px; margin: 16px 0; border-radius: 4px;">
            <p style="margin: 0; font-size: 13px; color: #991b1b;">
              <strong>Acción Inmediata Requerida:</strong> Verifique el stock disponible en bodega o la compensación financiera hacia el cliente desde el panel de administración.
            </p>
          </div>
        </div>
        <div style="background-color: #f9fafb; padding: 12px; text-align: center; font-size: 12px; color: #9ca3af; border-top: 1px solid #f3f4f6;">
          Monchis Café — Notificación Automática Transaccional
        </div>
      </div>
    `;

    return this.sendMail({ to: adminEmail, subject, html });
  }

  /**
   * Alerta Preventiva de Caducidad de Lotes de Café Especial Orgánico (Req 2.2)
   */
  public static async sendBatchExpiryAlert(payload: BatchExpiryAlertPayload): Promise<EmailSendResult> {
    const adminEmail = this.getAdminRecipient();
    const urgencia = payload.diasRestantes <= 5 ? 'URGENTE' : 'PREVENTIVA';
    const subject = `⚠️ [CADUCIDAD ${urgencia}] Lote #${payload.numeroLote} - ${payload.productoNombre} (${payload.diasRestantes} días restantes)`;

    const html = `
      <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #fed7aa; border-radius: 8px; overflow: hidden;">
        <div style="background-color: #f97316; color: white; padding: 20px; text-align: center;">
          <h2 style="margin: 0; font-size: 20px;">☕ Alerta de Caducidad de Lote de Café</h2>
          <p style="margin: 5px 0 0; font-size: 14px; opacity: 0.9;">Control de Calidad y Trazabilidad Sanitaria</p>
        </div>
        <div style="padding: 24px; background-color: #ffffff; color: #1f2937;">
          <p style="font-size: 15px; line-height: 1.5;">El siguiente lote de café orgánico está próximo a alcanzar su fecha límite de consumo óptimo:</p>
          
          <table style="width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px;">
            <tr style="border-bottom: 1px solid #f3f4f6;">
              <td style="padding: 8px; font-weight: bold; color: #4b5563;">Número de Lote:</td>
              <td style="padding: 8px; font-family: monospace; color: #ea580c; font-weight: bold;">${payload.numeroLote}</td>
            </tr>
            <tr style="border-bottom: 1px solid #f3f4f6;">
              <td style="padding: 8px; font-weight: bold; color: #4b5563;">Variedad / Producto:</td>
              <td style="padding: 8px; color: #111827;">${payload.productoNombre}</td>
            </tr>
            ${payload.fincaOrigen ? `
            <tr style="border-bottom: 1px solid #f3f4f6;">
              <td style="padding: 8px; font-weight: bold; color: #4b5563;">Finca de Origen:</td>
              <td style="padding: 8px; color: #374151;">${payload.fincaOrigen}</td>
            </tr>` : ''}
            <tr style="border-bottom: 1px solid #f3f4f6;">
              <td style="padding: 8px; font-weight: bold; color: #4b5563;">Fecha de Caducidad:</td>
              <td style="padding: 8px; color: #dc2626; font-weight: bold;">${payload.fechaCaducidad}</td>
            </tr>
            <tr>
              <td style="padding: 8px; font-weight: bold; color: #4b5563;">Días Restantes:</td>
              <td style="padding: 8px; color: #ea580c; font-weight: bold; font-size: 16px;">${payload.diasRestantes} días</td>
            </tr>
          </table>

          <div style="background-color: #fff7ed; border-left: 4px solid #f97316; padding: 12px; margin: 16px 0; border-radius: 4px;">
            <p style="margin: 0; font-size: 13px; color: #9a3412;">
              <strong>Recomendación:</strong> Priorice este lote para servicio en barra o trasládelo a promociones de rotación rápida para evitar mermas.
            </p>
          </div>
        </div>
        <div style="background-color: #f9fafb; padding: 12px; text-align: center; font-size: 12px; color: #9ca3af; border-top: 1px solid #f3f4f6;">
          Monchis Café — Trazabilidad Regional Chiapas & Veracruz
        </div>
      </div>
    `;

    return this.sendMail({ to: adminEmail, subject, html });
  }

  /**
   * Alerta de Inventario Crítico por Debajo del Stock Mínimo (Req 2.2)
   */
  public static async sendLowStockAlert(payload: LowStockAlertPayload): Promise<EmailSendResult> {
    const adminEmail = this.getAdminRecipient();
    const subject = `📦 [INVENTARIO BAJO] Stock crítico en: ${payload.productoNombre}`;

    const html = `
      <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #fde047; border-radius: 8px; overflow: hidden;">
        <div style="background-color: #eab308; color: white; padding: 20px; text-align: center;">
          <h2 style="margin: 0; font-size: 20px;">📦 Alerta de Stock Mínimo</h2>
          <p style="margin: 5px 0 0; font-size: 14px; opacity: 0.9;">Monchis Café — Reabastecimiento de Insumos</p>
        </div>
        <div style="padding: 24px; background-color: #ffffff; color: #1f2937;">
          <p style="font-size: 15px; line-height: 1.5;">El producto <strong>${payload.productoNombre}</strong> ha cruzado el umbral mínimo de seguridad en existencia.</p>
          
          <table style="width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px;">
            <tr style="border-bottom: 1px solid #f3f4f6;">
              <td style="padding: 8px; font-weight: bold; color: #4b5563;">Producto:</td>
              <td style="padding: 8px; color: #111827;">${payload.productoNombre}</td>
            </tr>
            <tr style="border-bottom: 1px solid #f3f4f6;">
              <td style="padding: 8px; font-weight: bold; color: #4b5563;">Stock Actual:</td>
              <td style="padding: 8px; color: #dc2626; font-weight: bold; font-size: 16px;">${payload.stockActual} unidades</td>
            </tr>
            <tr>
              <td style="padding: 8px; font-weight: bold; color: #4b5563;">Stock Mínimo Requerido:</td>
              <td style="padding: 8px; color: #4b5563;">${payload.stockMinimo} unidades</td>
            </tr>
          </table>

          <div style="background-color: #fefce8; border-left: 4px solid #eab308; padding: 12px; margin: 16px 0; border-radius: 4px;">
            <p style="margin: 0; font-size: 13px; color: #854d0e;">
              <strong>Acción sugerida:</strong> Contacte a los proveedores regionales para solicitar nuevo pedido de café o insumos comerciales.
            </p>
          </div>
        </div>
        <div style="background-color: #f9fafb; padding: 12px; text-align: center; font-size: 12px; color: #9ca3af; border-top: 1px solid #f3f4f6;">
          Monchis Café — Gestión Automatizada de Almacén
        </div>
      </div>
    `;

    return this.sendMail({ to: adminEmail, subject, html });
  }

  /**
   * Recibo / Confirmación de Compra para el Cliente (Req 2.3 & 2.4)
   */
  public static async sendOrderReceipt(payload: OrderReceiptPayload): Promise<EmailSendResult> {
    const subject = `☕ Monchis Café — Comprobante de Compra #${payload.ordenId.substring(0, 8)}`;

    const itemsHtml = payload.items
      .map(
        (item) => `
        <tr style="border-bottom: 1px solid #f3f4f6;">
          <td style="padding: 8px; color: #374151;">${item.cantidad}x ${item.nombre}</td>
          <td style="padding: 8px; text-align: right; color: #111827; font-weight: bold;">$${item.subtotal.toFixed(2)} MXN</td>
        </tr>
      `
      )
      .join('');

    const html = `
      <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #d1fae5; border-radius: 8px; overflow: hidden;">
        <div style="background-color: #059669; color: white; padding: 20px; text-align: center;">
          <h2 style="margin: 0; font-size: 20px;">☕ ¡Gracias por tu compra en Monchis Café!</h2>
          <p style="margin: 5px 0 0; font-size: 14px; opacity: 0.9;">Tu café de especialidad preparado con pasión</p>
        </div>
        <div style="padding: 24px; background-color: #ffffff; color: #1f2937;">
          <p style="font-size: 15px;">Hola, te compartimos el resumen de tu consumo con folio <strong>#${payload.ordenId}</strong>:</p>
          
          <table style="width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px;">
            <thead>
              <tr style="background-color: #f9fafb; border-bottom: 2px solid #e5e7eb;">
                <th style="padding: 8px; text-align: left; color: #4b5563;">Concepto</th>
                <th style="padding: 8px; text-align: right; color: #4b5563;">Subtotal</th>
              </tr>
            </thead>
            <tbody>
              ${itemsHtml}
            </tbody>
            <tfoot>
              <tr>
                <td style="padding: 12px 8px; font-weight: bold; font-size: 16px; color: #111827;">Total Pagado (${payload.metodoPago}):</td>
                <td style="padding: 12px 8px; text-align: right; font-weight: bold; font-size: 18px; color: #059669;">$${payload.total.toFixed(2)} MXN</td>
              </tr>
            </tfoot>
          </table>

          ${payload.sellosAcumulados !== undefined || payload.puntosGanados !== undefined ? `
          <div style="background-color: #ecfdf5; border: 1px dashed #10b981; padding: 12px; margin: 16px 0; border-radius: 6px; text-align: center;">
            <p style="margin: 0; font-size: 14px; color: #065f46; font-weight: bold;">🌟 Beneficios Monchis Rewards Acumulados</p>
            <p style="margin: 4px 0 0; font-size: 13px; color: #047857;">
              ${payload.sellosAcumulados !== undefined ? `Sellos activos: <strong>${payload.sellosAcumulados}/7</strong> (El 8vo café es gratis) • ` : ''}
              ${payload.puntosGanados !== undefined ? `Puntos ganados: <strong>+${payload.puntosGanados} pts</strong>` : ''}
            </p>
          </div>` : ''}
        </div>
        <div style="background-color: #f9fafb; padding: 12px; text-align: center; font-size: 12px; color: #9ca3af; border-top: 1px solid #f3f4f6;">
          Monchis Café — Gracias por apoyar el café orgánico sustentable
        </div>
      </div>
    `;

    return this.sendMail({ to: payload.clienteEmail, subject, html });
  }

  private static async sendMail(options: {
    to: string;
    subject: string;
    html: string;
  }): Promise<EmailSendResult> {
    try {
      const transporter = this.getTransporter();
      const mailOptions = {
        from: this.getFromAddress(),
        to: options.to,
        subject: options.subject,
        html: options.html,
      };

      const info = await transporter.sendMail(mailOptions);

      // Guardar en log para pruebas y auditoría
      EMAILS_SENT_LOG.push({
        to: options.to,
        subject: options.subject,
        html: options.html,
        timestamp: new Date().toISOString(),
      });

      return {
        success: true,
        messageId: info.messageId || 'mock-message-id',
      };
    } catch (error: any) {
      console.error('❌ [EmailService] Error al enviar correo:', error);
      return {
        success: false,
        error: error.message || 'Error desconocido al enviar correo SMTP',
      };
    }
  }
}
