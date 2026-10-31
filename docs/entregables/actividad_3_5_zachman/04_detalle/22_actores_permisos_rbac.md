# Nivel 4: DETALLE — Foco: QUIÉN
## Actores, Permisos y Responsabilidades (Matriz RBAC) — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

En la seguridad de la información y el diseño de sistemas distribuidos, el Control de Acceso Basado en Roles (**RBAC** - *Role-Based Access Control*) es el estándar de referencia para gestionar los permisos de los usuarios en una organización (Ferraiolo et al., 2001). En lugar de asignar permisos individuales usuario por usuario (lo que resulta insostenible y propenso a errores humanos), los privilegios se asocian formalmente a roles específicos del negocio, y cada empleado recibe únicamente los accesos indispensables para realizar su trabajo. Este enfoque se fundamenta en el clásico **Principio del Menor Privilegio** (*Principle of Least Privilege*) formulado por Saltzer y Schroeder (1975), el cual establece que todo programa o usuario debe operar empleando el conjunto mínimo de privilegios requeridos para cumplir su función.

Dentro de la Matriz de Zachman (1987), la celda **Detalle - Quién** aborda la seguridad y la asignación de permisos desde la perspectiva del constructor (*Security & Access Control Model / Builder's View*). En este nivel del código físico, formalizamos la **Matriz RBAC** que regula qué rutas de la API de Next.js y qué pantallas del frontend de Vue 3 puede ejecutar cada rol (`ADMIN`, `CAJERO`, `CLIENTE`, `INVITADO`), verificada de manera estricta mediante claims firmados en tokens JWT.

---

### 2. Estructura de Roles del Sistema

Los roles admitidos por el sistema se definen mediante la enumeración TypeScript `UserRole`:

```typescript
export enum UserRole {
  ADMIN = 'ADMIN',       // Dueño / Gerente general de la cafetería
  CAJERO = 'CAJERO',     // Barista u operador del punto de venta en mostrador
  CLIENTE = 'CLIENTE',   // Usuario registrado en el programa Monchis Rewards
  INVITADO = 'INVITADO'  // Visitante anónimo navegando el sitio web público
}
```

---

### 3. Matriz Formal de Permisos RBAC (Endpoints API y Vistas)

La siguiente matriz define las operaciones permitidas sobre cada recurso del sistema:
* **C:** Crear (POST) | **R:** Leer / Consultar (GET) | **U:** Actualizar (PUT / PATCH) | **D:** Desactivar / Eliminar (DELETE) | **X:** No Permitido (HTTP 403 Forbidden).

| Recurso / Módulo | Endpoint / Ruta | INVITADO | CLIENTE | CAJERO | ADMINISTRADOR |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Catálogo Público** | `GET /api/products` | **R** | **R** | **R** | **R** |
| **Gestión de Productos** | `POST, PUT, DELETE /api/products/*` | **X** | **X** | **X** | **C, U, D** |
| **Trazabilidad Lotes** | `GET, POST /api/inventory/batches` | **X** | **X** | **R** (Lectura) | **C, R, U** |
| **Órdenes POS** | `POST /api/pos/orders` | **X** | **X** | **C** (Cobro) | **C** (Cobro) |
| **Consulta de Órdenes**| `GET /api/pos/orders/*` | **X** | **R** (Propias) | **R** (Turno) | **R** (Todas) |
| **Corte de Caja Z** | `POST /api/admin/cash-cut` | **X** | **X** | **C** (Arqueo) | **C, R** (Auditoría) |
| **Analítica y UTM** | `GET /api/admin/analytics` | **X** | **X** | **X** | **R** (Completo) |
| **Auditoría DLQ** | `GET /api/admin/audit/dlq` | **X** | **X** | **X** | **R** |
| **Alertas Sanitarias** | `POST /api/admin/notifications/*` | **X** | **X** | **X** | **C, R** |
| **Configuración 2FA** | `POST /api/auth/2fa/*` | **X** | **X** | **X** | **C, R, U** |
| **Login y Refresh** | `POST /api/auth/login`, `/refresh` | **C** | **C** | **C** | **C** |
| **Logout (Revocación)**| `POST /api/auth/logout` | **X** | **C** | **C** | **C** |

---

### 4. Implementación Técnica en Código

Para garantizar que ningún usuario se salte los controles de acceso, el sistema implementa una doble barrera de seguridad:

#### 4.1 En la Capa de Backend (Middleware API):
Cada endpoint protegido pasa por el middleware `requireAuth` y `requireRole`. Los claims del usuario vienen firmados criptográficamente en el Access Token JWT:
```typescript
// Fragmento de apps/api/src/middleware/authMiddleware.ts
export function requireRole(allowedRoles: UserRole[]) {
  return (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
    if (!req.user || !allowedRoles.includes(req.user.rol)) {
      return res.status(403).json({
        error: 'Acceso Denegado: Su rol no cuenta con los permisos necesarios para esta operación.'
      });
    }
    next();
  };
}
```

#### 4.2 En la Capa de Frontend (Navigation Guards):
En Vue Router, antes de renderizar cualquier pantalla privada, se comprueba la meta-información de la ruta:
```typescript
// Fragmento de apps/web/src/router/index.ts
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({ path: '/login', query: { redirect: to.fullPath } });
  }
  if (to.meta.roles && !to.meta.roles.includes(authStore.user?.rol)) {
    return next({ path: '/pos' }); // Redirección segura
  }
  next();
});
```

---

### 5. Justificación Práctica en el Proyecto

Aplicar el principio del menor privilegio mediante una matriz RBAC formal es la diferencia entre un software casero y un sistema profesional. Como advierten Saltzer y Schroeder (1975), permitir que cualquier empleado tenga acceso a cambiar precios o borrar registros de caja tienta a la manipulación y deja al dueño del negocio indefenso ante desfalcos. En Monchis Café, garantizar que los baristas solo puedan registrar ventas y que la configuración de lotes campesinos y analítica financiera esté blindada exclusivamente para el Administrador con 2FA es lo que asegura la tranquilidad contable y legal de la empresa.

---

### 6. Referencias Bibliográficas

1. **Ferraiolo, D. F., Sandhu, R., Gavrila, S., Kuhn, D. R., & Chandramouli, R. (2001).** Proposed NIST standard for role-based access control. *ACM Transactions on Information and System Security (TISSEC)*, 4(3), 224–274. https://doi.org/10.1145/501978.501980
2. **Pressman, R. S., & Maxim, B. R. (2021).** *Ingeniería de software: un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
3. **Saltzer, J. H., & Schroeder, M. D. (1975).** The protection of information in computer systems. *Proceedings of the IEEE*, 63(9), 1278–1308. https://doi.org/10.1109/PROC.1975.9939
4. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

