# Base de Conocimiento del Producto — Brokitech Turnos

**Versión del documento:** 3.2
**Última actualización:** 26 de julio de 2026
**Responsable:** Equipo de Producto, Brokitech

---

## 1. Qué es Brokitech Turnos

Brokitech Turnos es una plataforma SaaS de gestión de turnos con cobro de seña anticipada por WhatsApp, diseñada para negocios de servicios en Argentina: peluquerías, barberías, centros de estética, consultorios odontológicos, kinesiología, estudios de tatuajes, veterinarias y talleres mecánicos.

El problema que resuelve es concreto: **el ausentismo sin aviso** (conocido como "no-show"). Según nuestra medición interna sobre 1.240 cuentas activas, un negocio de servicios pierde en promedio entre el 18% y el 27% de su facturación potencial por turnos que el cliente reserva y no cumple. Brokitech Turnos reduce ese número a un promedio del 4,1% al exigir una seña previa a confirmar el turno.

### 1.1 Propuesta de valor en una línea

Reservás por WhatsApp, pagás la seña por Mercado Pago, y el turno queda confirmado automáticamente en la agenda del negocio.

### 1.2 A quién NO está dirigido

- Negocios que venden productos físicos sin componente de turno (usar Brokitech CRM).
- Empresas que necesitan facturación electrónica AFIP integrada (está en roadmap, no disponible al día de hoy).
- Operaciones fuera de Argentina. Al día de la fecha solo operamos con Mercado Pago Argentina y números de WhatsApp con prefijo +54.

---

## 2. Arquitectura funcional

### 2.1 Los cuatro módulos

| Módulo | Función | Disponible desde el plan |
|---|---|---|
| **Agenda** | Calendario por profesional, bloqueos, feriados, horarios partidos | Inicial |
| **WhatsApp Bot** | Reserva conversacional, recordatorios, cancelaciones | Inicial |
| **Cobros** | Seña por Mercado Pago, reembolsos, conciliación | Inicial |
| **Analítica** | Tasa de no-show, ocupación, ingresos por profesional | Profesional |

### 2.2 Flujo de una reserva

1. El cliente final escribe al número de WhatsApp del negocio.
2. El bot identifica la intención de reservar y ofrece servicios disponibles.
3. El cliente elige servicio, profesional (opcional) y franja horaria.
4. El sistema **pre-reserva** el slot y lo bloquea por 15 minutos.
5. Se envía un link de pago de Mercado Pago por el monto de la seña.
6. Al acreditarse el pago, el turno pasa a estado **confirmado** y se envía el comprobante.
7. Si no se paga en 15 minutos, la pre-reserva se libera automáticamente.

> **Importante:** el slot nunca se ocupa definitivamente antes del pago. Esto evita que un cliente bloquee la agenda sin intención real de asistir.

### 2.3 Estados de un turno

- `pendiente_pago` — pre-reservado, esperando la seña. Expira a los 15 minutos.
- `confirmado` — seña acreditada.
- `recordado` — se envió el recordatorio de 24 h.
- `completado` — el negocio marcó asistencia.
- `no_show` — el cliente no asistió. La seña **no** se reintegra.
- `cancelado_cliente` — cancelado por el cliente. Reintegro según política de cancelación del negocio.
- `cancelado_negocio` — cancelado por el negocio. Reintegro del 100% siempre.

---

## 3. Cobro de señas

### 3.1 Configuración del monto

Cada servicio puede tener su seña definida de tres formas:

- **Monto fijo** — por ejemplo, $5.000 ARS por corte de pelo.
- **Porcentaje del precio del servicio** — por ejemplo, 30% de $25.000 = $7.500 ARS.
- **Sin seña** — el turno se confirma sin pago. Útil para clientes recurrentes de confianza.

La configuración se hace por servicio en *Configuración → Servicios → Editar → Política de seña*.

### 3.2 Comisiones

Brokitech Turnos **no cobra comisión sobre las señas**. El dinero va directo a la cuenta de Mercado Pago del negocio. La única comisión aplicable es la de Mercado Pago (actualmente 6,29% + IVA para acreditación inmediata, sujeta a los aranceles vigentes de Mercado Pago, que no controlamos).

### 3.3 Reembolsos

Los reembolsos se procesan desde el panel en *Turnos → Ver turno → Reintegrar seña*. El dinero vuelve al medio de pago original en un plazo de 3 a 10 días hábiles, según defina Mercado Pago. Brokitech no retiene fondos en ningún momento.

---

## 4. WhatsApp: requisitos y limitaciones

### 4.1 Qué número se puede usar

Se requiere un número de teléfono que **no esté registrado en WhatsApp ni en WhatsApp Business** al momento de la conexión. Recomendamos usar una línea dedicada al negocio.

Trabajamos sobre la **WhatsApp Cloud API oficial de Meta**. No usamos librerías no oficiales ni automatización del cliente de escritorio, lo cual significa que la cuenta no corre riesgo de bloqueo por violación de términos.

### 4.2 Ventana de 24 horas

Meta permite responder libremente a un cliente durante las 24 horas posteriores a su último mensaje. Fuera de esa ventana solo se pueden enviar **plantillas pre-aprobadas**. Brokitech Turnos incluye 4 plantillas ya aprobadas:

1. `recordatorio_turno_24h`
2. `confirmacion_turno`
3. `turno_cancelado_negocio`
4. `link_pago_sena`

Las plantillas adicionales requieren aprobación de Meta y demoran entre 1 y 48 horas.

### 4.3 Costos de mensajería

Meta cobra por conversación iniciada por el negocio (categoría *utility* en Argentina, aproximadamente USD 0,034 por conversación al día de la fecha). Los planes incluyen un cupo mensual de conversaciones salientes; el excedente se factura a costo, sin margen.

---

## 5. Integraciones disponibles

| Integración | Estado | Plan mínimo |
|---|---|---|
| Mercado Pago (Checkout Pro) | Disponible | Inicial |
| WhatsApp Cloud API | Disponible | Inicial |
| Google Calendar (sincronización bidireccional) | Disponible | Profesional |
| Exportación CSV / Excel | Disponible | Inicial |
| Webhooks salientes | Disponible | Negocio |
| API REST pública | Disponible | Negocio |
| Instagram Direct | En beta cerrada | Negocio |
| Facturación AFIP | En roadmap (Q4 2026) | — |
| Stripe / pagos internacionales | No planificado | — |

---

## 6. Onboarding

El alta de una cuenta nueva toma en promedio **35 minutos** y consta de cinco pasos:

1. Crear la cuenta con email y validar.
2. Cargar servicios, duraciones y precios.
3. Cargar profesionales y sus horarios.
4. Conectar Mercado Pago (OAuth, un clic).
5. Conectar WhatsApp (verificación del número por SMS o llamada).

Los planes Profesional y Negocio incluyen una sesión de onboarding asistido por videollamada de 45 minutos, sin costo adicional.

---

## 7. Límites técnicos del sistema

- Máximo de 200 servicios por cuenta.
- Máximo de 90 días de anticipación para reservar un turno.
- Duración mínima de un turno: 5 minutos. Máxima: 8 horas.
- Retención de historial de turnos: 36 meses.
- Tamaño máximo de importación CSV de clientes: 10.000 filas por archivo.
- Los recordatorios automáticos se envían a las 24 h y a las 3 h previas al turno.

---

## 8. Disponibilidad y soporte técnico

- **SLA de disponibilidad:** 99,5% mensual en plan Negocio; sin SLA contractual en Inicial y Profesional (disponibilidad medida histórica: 99,7%).
- **Ventanas de mantenimiento:** martes de 03:00 a 05:00 (hora de Argentina), anunciadas con 48 h de anticipación.
- **Estado del servicio:** publicado en status.brokitech.com

---

## 9. Glosario

- **No-show:** turno reservado al que el cliente no asiste ni avisa.
- **Seña:** pago parcial anticipado que confirma la reserva.
- **Slot:** franja horaria discreta de la agenda.
- **Ventana de 24 h:** período durante el cual WhatsApp permite mensajes libres tras el último mensaje del cliente.
- **Plantilla (template):** mensaje pre-aprobado por Meta para iniciar conversaciones.
- **Pre-reserva:** bloqueo temporal de 15 minutos mientras se espera el pago de la seña.
