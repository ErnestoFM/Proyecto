# Nivel 3: ALTO NIVEL — Foco: POR QUÉ
## Reglas del Negocio y Prioridades del Proyecto — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

Una regla de negocio es una directiva, política o restricción formal que define o restringe algún aspecto de la estructura o el comportamiento de la empresa (Business Rules Group [BRG], 2000). Como destaca Ross (2003), las reglas de negocio existen con independencia del software; pertenecen a las políticas del dueño de la empresa y dictan cómo se debe cobrar, cómo se rota el producto y qué condiciones de seguridad deben cumplirse para proteger los activos del negocio. Si las reglas de negocio no se formalizan en el diseño de alto nivel, los programadores terminan codificando su propia interpretación en el backend, provocando vulnerabilidades lógicas y discrepancias contables (Pressman & Maxim, 2021).

Dentro de la Matriz de Zachman (1987), la celda **Alto Nivel - Por qué** vincula las políticas y motivaciones del negocio con el modelo lógico del sistema (*Business Rules & Priorities / Designer's View*). En este nivel respondemos a la pregunta: *¿Cuáles son las reglas inquebrantables que gobiernan los casos de uso y qué prioridad tienen en el proyecto?* Para **Monchis Café**, estas reglas son las que garantizan que nadie manipule precios desde el navegador, que el café orgánico rote de forma fresca (PEPS), que el bono ecológico se aplique correctamente y que la caja no sufra fugas de efectivo.

---

### 2. Catálogo Oficial de Reglas de Negocio (RN-01 a RN-08)

A continuación se detallan las ocho reglas de negocio formales de la cafetería, con su lógica de aplicación y su prioridad en la arquitectura:

```
+=======================================================================================+
|                          REGLAS DE NEGOCIO — MONCHIS CAFÉ                             |
+=======================================================================================+
| RN-01: Integridad de Precios Oficiales (Servidor)  | RN-05: 2FA Obligatorio para Admin|
| RN-02: Rotación Estricta de Inventario PEPS        | RN-06: Transacción Compensatoria |
| RN-03: Bonificación Ecológica ODS 12 por Termo     | RN-07: Límite Anti-Fuerza Bruta  |
| RN-04: Límites de Lealtad en Monchis Rewards       | RN-08: Arqueo Ciego en Corte Z   |
+=======================================================================================+
```

---

#### RN-01: Integridad de Precios Oficiales de Catálogo
* **Declaración de la Regla:** El cálculo de los subtotales, impuestos y totales de cualquier venta debe realizarse **estrictamente en el servidor** consultando la base de datos oficial.
* **Restricción Técnica:** Se prohíbe taxativamente aceptar precios unitarios enviados en el cuerpo JSON de peticiones del frontend. Si el cliente web envía una alteración de precio, el backend la sobreescribe con el precio vigente en `Product.precio`.
* **Prioridad en el Proyecto:** **CRÍTICA (P1)**. Evita fraudes de alteración de precios en el mostrador.

#### RN-02: Rotación de Inventarios PEPS (Primeras Entradas, Primeras Salidas)
* **Declaración de la Regla:** El consumo de insumos de café orgánico y alimentos perecederos debe descontarse automáticamente del **lote con fecha de ingreso o tostado más antigua** que aún cuente con existencias positivas.
* **Restricción Técnica:** Ningún barista o cajero puede elegir manualmente qué lote descontar en el POS; el sistema ejecuta una consulta ordenada por `fechaIngreso ASC` en `Batch`.
* **Prioridad en el Proyecto:** **ALTA (P2)**. Cumple con la Meta 12.3 de los ODS (reducción de mermas).

#### RN-03: Bonificación Ecológica por Recipiente Reusable (ODS 12)
* **Declaración de la Regla:** El descuento de **\$5.00 MXN** o la asignación de sellos dobles solo es aplicable cuando el cliente presenta físicamente una taza o termo reutilizable en la barra de atención.
* **Restricción Técnica:** La activación requiere que el cajero marque la casilla explícita en la orden. El sistema registra esta condición en la tabla `Order` para auditar el ahorro de vasos plásticos.
* **Prioridad en el Proyecto:** **ALTA (P2)**. Eje rector de sostenibilidad (Meta 12.5 de los ODS).

#### RN-04: Límites y Canje en "Monchis Rewards"
* **Declaración de la Regla:** Cada bebida preparada pagada otorga exactamente **1 sello digital**. Al acumular 7 sellos verificados, el sistema otorga la **8va bebida de cortesía (\$0.00)**.
* **Restricción Técnica:** Los sellos son intransferibles entre cuentas de clientes. El sistema no permite acumular sellos en compras donde la bebida ya fue bonificada como cortesía.
* **Prioridad en el Proyecto:** **MEDIA (P3)**. Fidelización y retención de clientela.

#### RN-05: Segundo Factor de Autenticación (2FA / TOTP) para Administrador
* **Declaración de la Regla:** Toda cuenta con perfil `ADMIN` debe ingresar obligatoriamente un código criptográfico de 6 dígitos (RFC 6238) para emitir el Access Token final.
* **Restricción Técnica:** La ventana de tolerancia del código TOTP es de $\pm 30$ segundos. No se admiten bypasses ni tokens de prueba en ambiente de producción.
* **Prioridad en el Proyecto:** **CRÍTICA (P1)**. Seguridad patrimonial y protección de datos gerenciales.

#### RN-06: Compensación Transaccional Automática (Saga de Reversa)
* **Declaración de la Regla:** Si una orden es cobrada pero no puede prepararse debido a un desabasto inesperado del grano orgánico, el sistema debe orquestar automáticamente la reversa y el reembolso íntegro al cliente.
* **Restricción Técnica:** El evento se procesa mediante RabbitMQ (`cafeteria.events`). Si falla la compensación tras 3 intentos, se desvía a la `orders.dlq` con alerta SMTP inmediata.
* **Prioridad en el Proyecto:** **ALTA (P2)**. Consistencia transaccional y satisfacción del cliente.

#### RN-07: Mitigación de Fuerza Bruta en Autenticación
* **Declaración de la Regla:** Ninguna dirección IP puede emitir más de **5 intentos fallidos consecutivos de acceso** en un periodo de 15 minutos sin ser bloqueada temporalmente.
* **Restricción Técnica:** Control de tasa (*Rate Limiting*) en memoria/Redis en las rutas `/api/auth/login` y `/api/auth/refresh`.
* **Prioridad en el Proyecto:** **CRÍTICA (P1)**. Protección contra ataques de diccionario y bots.

#### RN-08: Arqueo Ciego en Corte de Caja Diario
* **Declaración de la Regla:** Al momento del corte de turno (*Reporte Z*), el cajero debe declarar físicamente el dinero en efectivo que tiene en caja **antes** de que el sistema le revele el monto esperado según las ventas registradas.
* **Restricción Técnica:** El sistema no muestra el saldo teórico acumulado en la pantalla de arqueo hasta que el cajero confirma el conteo de billetes y monedas.
* **Prioridad en el Proyecto:** **ALTA (P2)**. Prevención de robos hormiga y cuadre transparente de caja.

---

### 3. Matriz de Prioridades de Implementación en el Proyecto

| Nivel de Prioridad | Reglas de Negocio Asociadas | Criterio de Decisión Arquitectónica | Momento de Entrega |
| :--- | :--- | :--- | :---: |
| **P1 — CRÍTICA**<br>*(Bloqueante para Producción)* | **RN-01** (Precios Servidor)<br>**RN-05** (2FA Admin)<br>**RN-07** (Rate Limiting) | Sin estas reglas el sistema es vulnerable a robos, alteración de ventas y ataques cibernéticos. | Sprint 1 (Semana 1-4) |
| **P2 — ALTA**<br>*(Operación Sustentable y Caja)* | **RN-02** (Rotación PEPS)<br>**RN-03** (Bono Ecológico)<br>**RN-06** (Reversa Saga)<br>**RN-08** (Arqueo Ciego) | Son las reglas que garantizan la rentabilidad, el control de mermas y la diferenciación ODS 12. | Sprint 2 (Semana 5-8) |
| **P3 — MEDIA**<br>*(Fidelización y Marketing)* | **RN-04** (Monchis Rewards) | Incrementa la retención y recurrencia de compra en la sucursal física. | Sprint 3 (Semana 9-12) |

---

### 4. Justificación Práctica en el Proyecto

Formalizar las reglas de negocio en la Matriz de Zachman asegura que las políticas de la cafetería queden plasmadas en código ejecutable y no se queden en un reglamento pegado en la pared que nadie lee. Como señala Ross (2003), una regla de negocio que no se automatiza es una regla que tarde o temprano se rompe. En Monchis Café, blindar el cálculo de precios en el backend (RN-01) y obligar al arqueo ciego (RN-08) garantiza que los dueños duerman tranquilos sabiendo que cada peso que ingresa a la cafetería está respaldado por el sistema.

---

### 5. Referencias Bibliográficas

1. **Business Rules Group. (2000).** *Defining Business Rules ~ What Are They Really?* (4.ª ed.). BRG. http://www.businessrulesgroup.org
2. **Pressman, R. S., & Maxim, B. R. (2021).** *Ingeniería de software: un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
3. **Ross, R. G. (2003).** *Principles of the Business Rule Approach*. Addison-Wesley Professional.
4. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

