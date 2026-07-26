# FAQ de Soporte — Brokitech Turnos

**Versión del documento:** 3.2
**Última actualización:** 26 de julio de 2026
**Canal de soporte:** soporte@brokitech.com — WhatsApp +54 9 11 5555-0143

---

## A. Cuenta y facturación

### A1. ¿Cómo empiezo? ¿Hay prueba gratuita?
Sí. Todos los planes incluyen **14 días de prueba gratuita** con funcionalidad completa, sin tarjeta de crédito. Al finalizar la prueba, si no cargás un medio de pago, la cuenta pasa a modo lectura: podés ver tus datos y exportarlos, pero el bot deja de tomar reservas.

### A2. ¿Puedo cambiar de plan en cualquier momento?
Sí. Los cambios de plan son inmediatos.
- **Upgrade:** se cobra la diferencia prorrateada por los días restantes del ciclo.
- **Downgrade:** se aplica al inicio del siguiente ciclo de facturación. No se emiten reintegros por downgrade.

### A3. ¿Cómo cancelo mi suscripción?
Desde *Configuración → Suscripción → Cancelar plan*. La cancelación es efectiva al final del ciclo ya pagado; seguís teniendo acceso hasta esa fecha. No hay período de permanencia mínima ni penalidad por cancelación.

### A4. ¿Qué pasa con mis datos si cancelo?
Conservamos tus datos en modo lectura durante **60 días** desde la cancelación, para que puedas exportarlos. Pasados los 60 días se eliminan de forma permanente e irreversible. Podés pedir la eliminación inmediata escribiendo a privacidad@brokitech.com.

### A5. ¿Emiten factura?
Sí, factura tipo B o A según corresponda, emitida automáticamente y enviada por email dentro de las 72 h de acreditado el pago. Cargá tu CUIT en *Configuración → Datos de facturación* para recibir factura A.

### A6. ¿Qué medios de pago aceptan para la suscripción?
Tarjeta de crédito y débito (Visa, Mastercard, Amex) y débito automático vía Mercado Pago. No aceptamos transferencia bancaria salvo en plan Enterprise.

### A7. ¿Hay descuento por pago anual?
Sí, **20% de descuento** pagando 12 meses por adelantado.

---

## B. WhatsApp

### B1. ¿Puedo usar mi número actual de WhatsApp Business?
No directamente. El número debe estar libre de WhatsApp al momento de conectarlo a la Cloud API. Si querés conservar el mismo número, primero tenés que **eliminar la cuenta** de WhatsApp Business desde la app (Configuración → Cuenta → Eliminar mi cuenta), esperar unos minutos y luego conectarlo. Perdés el historial de chats previo. La mayoría de nuestros clientes prefiere dar de alta una línea nueva y dedicada.

### B2. ¿Me pueden bloquear el número?
Es muy poco probable. Usamos la API oficial de Meta, no automatización no oficial. Los bloqueos ocurren cuando los usuarios marcan tus mensajes como spam de forma sostenida. Para evitarlo: no envíes promociones no solicitadas y respetá las bajas.

### B3. El bot no responde a mis clientes. ¿Qué reviso?
En orden:
1. *Configuración → WhatsApp* — verificá que el estado diga **Conectado** (verde).
2. Revisá que el negocio no esté en *modo pausado* (*Configuración → General*).
3. Verificá que haya horarios cargados para el día en curso.
4. Revisá el estado de la cuenta de Meta en business.facebook.com — un rechazo de verificación de negocio suspende el envío.
5. Si todo lo anterior está bien, escribinos: mandá el número y la hora aproximada del mensaje que no se respondió.

### B4. ¿El bot entiende audios?
Sí. Transcribimos notas de voz de hasta 2 minutos. Audios más largos reciben una respuesta pidiendo que el cliente escriba el mensaje.

### B5. ¿Puedo intervenir manualmente una conversación?
Sí. Desde *Conversaciones* podés tomar el control de cualquier chat con el botón **Modo humano**. El bot deja de responder en ese chat durante 6 horas o hasta que lo devuelvas al modo automático.

---

## C. Señas y pagos

### C1. ¿Brokitech se queda con parte de la seña?
No. El 100% de la seña va a tu cuenta de Mercado Pago. Nosotros cobramos únicamente el abono mensual del plan. La única deducción es la comisión de Mercado Pago, que es de ellos, no nuestra.

### C2. Un cliente pagó pero el turno no se confirmó. ¿Qué hago?
Suele ser un retraso en el webhook de Mercado Pago. Esperá 5 minutos. Si sigue igual, entrá a *Turnos → Pendientes de pago* y usá **Reconciliar con Mercado Pago**: buscamos el pago por referencia externa y confirmamos el turno. Si el pago existe, se resuelve en el momento.

### C3. ¿Puedo reintegrar una seña?
Sí, total o parcialmente, desde *Turnos → Ver turno → Reintegrar seña*. El plazo de acreditación lo define Mercado Pago (3 a 10 días hábiles).

### C4. ¿Qué pasa si el cliente no viene?
El turno se marca como `no_show` y la seña queda para el negocio. Es tu decisión comercial reintegrarla o no; el sistema no lo hace automáticamente.

### C5. ¿Puedo cobrar el servicio completo por adelantado en lugar de una seña?
Sí. Configurá la seña como 100% del precio del servicio.

### C6. ¿Se puede reservar sin pagar seña?
Sí, configurando el servicio como "sin seña". También podés marcar clientes individuales como **confianza**, y a ellos no se les pedirá seña aunque el servicio la tenga configurada.

---

## D. Agenda

### D1. ¿Cómo cargo vacaciones o un feriado?
*Agenda → Bloqueos → Nuevo bloqueo*. Podés bloquear el negocio completo o un profesional específico, por rango de fechas. Los turnos ya confirmados dentro del bloqueo **no** se cancelan solos: el sistema te muestra la lista para que decidas.

### D2. ¿Soporta horarios partidos?
Sí. Por ejemplo, 09:00–13:00 y 16:00–20:00, distinto por día y por profesional.

### D3. ¿Se puede sobrevender un horario (overbooking)?
Por defecto no. Se puede habilitar overbooking controlado por servicio en *Servicios → Editar → Permitir superposición*, indicando cuántos turnos simultáneos admite.

### D4. ¿Se sincroniza con Google Calendar?
Sí, desde el plan Profesional. La sincronización es bidireccional: los eventos que crees en Google bloquean el horario en Brokitech, y los turnos de Brokitech aparecen en tu Google Calendar. La sincronización corre cada 5 minutos.

### D5. ¿Cuántos días de anticipación se puede reservar?
Hasta 90 días. El límite es configurable por servicio en *Servicios → Editar → Anticipación máxima*.

---

## E. Datos y seguridad

### E1. ¿Dónde se alojan mis datos?
En infraestructura de Oracle Cloud Infrastructure (OCI), región São Paulo (`sa-saopaulo-1`), con réplica de respaldo en Vinhedo (`sa-vinhedo-1`).

### E2. ¿Hacen backups?
Sí. Respaldo completo diario con retención de 30 días, y point-in-time recovery de 7 días.

### E3. ¿Pueden ver las conversaciones de mis clientes?
Solo personal técnico autorizado, únicamente ante un ticket de soporte abierto por vos, y queda registrado en un log de auditoría que podés solicitar. No usamos el contenido de tus conversaciones para entrenar modelos.

### E4. ¿Cumplen con la ley argentina de datos personales?
Sí, operamos bajo la Ley 25.326 de Protección de los Datos Personales. Ver la Política de Privacidad para el detalle.

### E5. ¿Puedo exportar todos mis datos?
Sí, en cualquier momento y sin costo, desde *Configuración → Exportar datos*. Se genera un ZIP con CSVs de clientes, turnos, pagos y servicios. Llega por email en menos de 15 minutos.

---

## F. Problemas frecuentes

### F1. "Error al conectar Mercado Pago"
Ocurre casi siempre por intentar conectar una cuenta de Mercado Pago que ya está vinculada a otra cuenta de Brokitech. Desvinculá primero desde la cuenta anterior, o usá otra cuenta de Mercado Pago.

### F2. Los recordatorios no llegan
Verificá que el cliente no haya bloqueado tu número y que la plantilla `recordatorio_turno_24h` figure como **aprobada** en *Configuración → WhatsApp → Plantillas*. Meta puede revocar la aprobación de una plantilla si recibe reportes de spam.

### F3. La agenda muestra horarios que ya pasaron como disponibles
Es un problema de zona horaria. Revisá *Configuración → General → Zona horaria* y ponela en `America/Argentina/Buenos_Aires`.

### F4. Importé un CSV de clientes y quedaron duplicados
La importación deduplica por número de teléfono en formato internacional (`+5491155550143`). Si tu CSV tiene números sin prefijo o con guiones, se importan como nuevos. Normalizá la columna teléfono y volvé a importar: los duplicados se pueden fusionar desde *Clientes → Herramientas → Fusionar duplicados*.

---

## G. Tiempos de respuesta del soporte

| Plan | Canal | Primera respuesta |
|---|---|---|
| Inicial | Email | Hasta 48 h hábiles |
| Profesional | Email + WhatsApp | Hasta 24 h hábiles |
| Negocio | Email + WhatsApp + teléfono | Hasta 4 h hábiles |
| Enterprise | Canal dedicado + Slack compartido | Hasta 1 h hábil |

Horario de atención: lunes a viernes de 09:00 a 18:00 (hora de Argentina). Las incidencias críticas (servicio caído) se atienden 24/7 en plan Negocio y Enterprise.
