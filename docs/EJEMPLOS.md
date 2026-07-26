# Ejemplos de preguntas y respuestas

> Archivo generado por `python scripts/generar_ejemplos.py`. 
> Las respuestas son la salida textual del agente, sin editar.

- **Generado:** 26/07/2026 13:43
- **Motor:** MODO DEMO (sin clave de API)
- **Fragmentos indexados:** 124

---

## 1. ¿Brokitech se queda con una parte de la seña que cobro?

**Modo demo (sin clave de API).** Extractos textuales de la documentación, sin redacción del modelo:

**1. FAQ de Soporte, pág. 2, sección «C1. ¿Brokitech se queda con parte de la seña?»**

> C1. ¿Brokitech se queda con parte de la seña?
No. El 100% de la seña va a tu cuenta de Mercado Pago. Nosotros cobramos únicamente el abono
mensual del plan. La única deducción es la comisión de Mercado Pago, que es de ellos, no
nuestra.

**2. Base de Conocimiento del Producto, pág. 1, sección «1.1 Propuesta de valor en una línea»**

> 1.1 Propuesta de valor en una línea
Reservás por WhatsApp, pagás la seña por Mercado Pago, y el turno queda confirmado
automáticamente en la agenda del negocio.

**3. Base de Conocimiento del Producto, pág. 1, sección «1. Qué es Brokitech Turnos»**

> 1. Qué es Brokitech Turnos
Brokitech Turnos es una plataforma SaaS de gestión de turnos con cobro de seña anticipada por
WhatsApp, diseñada para negocios de servicios en Argentina: peluquerías, barberías, centros de
estética, consultorios odontológicos, kinesiología, estudios de tatuajes, veterinarias y talleres
mecánicos.
El problema que resuelve es concreto: el ausentismo sin aviso (conocido como "no-show"). Según
nuestra medición interna sobre 1.240 cuentas activas, un negocio de servicios pierde en promedio
entre el 18% y el 27% de su facturación potencial por turnos que el cliente reserva y no cumple.
Brokitech Turnos reduce ese número a un promedio del 4,1% al exigir una seña previa a confirmar
el turno.


**Herramientas invocadas:**

1. `buscar_en_documentacion({'consulta': '¿Brokitech se queda con una parte de la seña que cobro?', 'top_k': 3})`

---

## 2. Somos 8 profesionales y hacemos unos 1200 turnos por mes. ¿Qué plan me conviene y cuánto pagaría?

**Modo demo (sin clave de API).** Extractos textuales de la documentación, sin redacción del modelo:

**1. Planes y Precios, pág. 2, sección «4. Excedentes»**

> 4. Excedentes
Los planes tienen cupos. Superarlos no interrumpe el servicio; se factura el excedente en el ciclo
siguiente:
Concepto
Costo del excedente
Turno adicional (planes Inicial y Profesional)
$95 por turno
Conversación saliente adicional de WhatsApp
$48 por conversación
Profesional adicional (plan Profesional)
$4.900 por mes
Profesional adicional (plan Negocio)
$3.900 por mes
Sucursal adicional (plan Negocio)
$19.900 por mes
El plan Negocio no tiene límite de turnos, por lo que no genera excedente por ese concepto.
Enviamos un aviso por email al alcanzar el 80% y el 100% del cupo mensual.

**2. Tabla comparativa de planes (CSV), pág. 1, sección «Plan Enterprise»**

> Plan Enterprise
plan: Enterprise; precio mensual ars: a medida; precio anual por mes ars: a medida; ahorro anual ars: a medida; profesionales incluidos: ilimitados; turnos por mes: ilimitados; servicios max: 200; conversaciones wa mes: a medida; usuarios panel: ilimitados; analitica: si; google calendar: si; onboarding asistido: si; white label: si; api rest: si; webhooks: si; multi sucursal: si; sla contractual: personalizado; soporte primera respuesta: 1 h habil; costo profesional adicional ars: a medida; costo turno excedente ars: 0; costo conversacion excedente ars: a medida; publico objetivo: Franquicias mas de 15 profesionales o infraestructura dedicada

**3. Tabla comparativa de planes (CSV), pág. 1, sección «Plan Profesional»**

> Plan Profesional
plan: Profesional; precio mensual ars: 39900; precio anual por mes ars: 31920; ahorro anual ars: 95760; profesionales incluidos: 5; turnos por mes: 800; servicios max: 60; conversaciones wa mes: 1500; usuarios panel: 8; analitica: si; google calendar: si; onboarding asistido: si; white label: no; api rest: no; webhooks: no; multi sucursal: no; sla contractual: no; soporte primera respuesta: 24 h habiles; costo profesional adicional ars: 4900; costo turno excedente ars: 95; costo conversacion excedente ars: 48; publico objetivo: Peluquerias y centros de estetica de 2 a 5 personas


**Herramientas invocadas:**

1. `buscar_en_documentacion({'consulta': 'Somos 8 profesionales y hacemos unos 1200 turnos por mes. ¿Qué plan me conviene y cuánto pagaría?', 'top_k': 3})`

---

## 3. ¿Puedo usar mi número actual de WhatsApp Business?

**Modo demo (sin clave de API).** Extractos textuales de la documentación, sin redacción del modelo:

**1. FAQ de Soporte, pág. 2, sección «B1. ¿Puedo usar mi número actual de WhatsApp Business?»**

> B1. ¿Puedo usar mi número actual de WhatsApp Business?
No directamente. El número debe estar libre de WhatsApp al momento de conectarlo a la Cloud
API. Si querés conservar el mismo número, primero tenés que eliminar la cuenta de WhatsApp
Business desde la app (Configuración -> Cuenta -> Eliminar mi cuenta), esperar unos minutos y
luego conectarlo. Perdés el historial de chats previo. La mayoría de nuestros clientes prefiere dar
de alta una línea nueva y dedicada.

**2. Base de Conocimiento del Producto, pág. 3, sección «4.1 Qué número se puede usar»**

> 4.1 Qué número se puede usar
Se requiere un número de teléfono que no esté registrado en WhatsApp ni en WhatsApp Business
al momento de la conexión. Recomendamos usar una línea dedicada al negocio.
Trabajamos sobre la WhatsApp Cloud API oficial de Meta. No usamos librerías no oficiales ni
automatización del cliente de escritorio, lo cual significa que la cuenta no corre riesgo de bloqueo
por violación de términos.

**3. FAQ de Soporte, pág. 2, sección «4. Revisá el estado de la cuenta de Meta en business.facebook.com — un rechazo de verificación»**

> 4. Revisá el estado de la cuenta de Meta en business.facebook.com — un rechazo de verificación
de negocio suspende el envío.


**Herramientas invocadas:**

1. `buscar_en_documentacion({'consulta': '¿Puedo usar mi número actual de WhatsApp Business?', 'top_k': 3})`

---

## 4. Si cancelo la suscripción, ¿cuánto tiempo tengo para exportar mis datos?

**Modo demo (sin clave de API).** Extractos textuales de la documentación, sin redacción del modelo:

**1. FAQ de Soporte, pág. 4, sección «E5. ¿Puedo exportar todos mis datos?»**

> E5. ¿Puedo exportar todos mis datos?
Sí, en cualquier momento y sin costo, desde Configuración -> Exportar datos. Se genera un ZIP
con CSVs de clientes, turnos, pagos y servicios. Llega por email en menos de 15 minutos.

**2. FAQ de Soporte, pág. 1, sección «A3. ¿Cómo cancelo mi suscripción?»**

> A3. ¿Cómo cancelo mi suscripción?
Desde Configuración -> Suscripción -> Cancelar plan. La cancelación es efectiva al final del ciclo
ya pagado; seguís teniendo acceso hasta esa fecha. No hay período de permanencia mínima ni
penalidad por cancelación.

**3. FAQ de Soporte, pág. 1, sección «A4. ¿Qué pasa con mis datos si cancelo?»**

> A4. ¿Qué pasa con mis datos si cancelo?
Conservamos tus datos en modo lectura durante 60 días desde la cancelación, para que puedas
exportarlos. Pasados los 60 días se eliminan de forma permanente e irreversible. Podés pedir la
eliminación inmediata escribiendo a privacidad@brokitech.com.


**Herramientas invocadas:**

1. `buscar_en_documentacion({'consulta': 'Si cancelo la suscripción, ¿cuánto tiempo tengo para exportar mis datos?', 'top_k': 3})`

---

## 5. ¿Qué diferencia hay entre el plan Profesional y el Negocio?

**Modo demo (sin clave de API).** Extractos textuales de la documentación, sin redacción del modelo:

**1. Planes y Precios, pág. 2, sección «4. Excedentes»**

> 4. Excedentes
Los planes tienen cupos. Superarlos no interrumpe el servicio; se factura el excedente en el ciclo
siguiente:
Concepto
Costo del excedente
Turno adicional (planes Inicial y Profesional)
$95 por turno
Conversación saliente adicional de WhatsApp
$48 por conversación
Profesional adicional (plan Profesional)
$4.900 por mes
Profesional adicional (plan Negocio)
$3.900 por mes
Sucursal adicional (plan Negocio)
$19.900 por mes
El plan Negocio no tiene límite de turnos, por lo que no genera excedente por ese concepto.
Enviamos un aviso por email al alcanzar el 80% y el 100% del cupo mensual.

**2. Base de Conocimiento del Producto, pág. 4, sección «5. Conectar WhatsApp (verificación del número por SMS o llamada).»**

> 5. Conectar WhatsApp (verificación del número por SMS o llamada).
Los planes Profesional y Negocio incluyen una sesión de onboarding asistido por videollamada de

**3. Planes y Precios, pág. 1, sección «2. Funcionalidades por plan»**

> 2. Funcionalidades por plan
Funcionalidad
Inicial
Profesional
Negocio
Enterprise
Agenda
multi-profesional
Si
Si
Si
Si
Bot de WhatsApp
Si
Si
Si
Si
Cobro de seña con
Mercado Pago
Si
Si
Si
Si
Recordatorios
automáticos
Si
Si
Si
Si
Exportación CSV /
Excel
Si
Si
Si
Si
Modo humano en
conversaciones
Si
Si
Si
Si
Panel de analítica y
no-show
—
Si
Si
Si
Sincronización con
Google Calendar
—
Si
Si
Si
Funcionalidad
Inicial
Profesional
Negocio
Enterprise
Onboarding asistido
por videollamada
—
Si
Si
Si
Marca propia en los
mensajes
(white-label)
—
—
Si
Si
API REST pública
—
—
Si
Si
Webhooks salientes
—
—
Si
Si
Múltiples sucursales
—
—
Si
Si
SLA 99,5%
contractual
—
—
Si
Si
Autenticación en dos
pasos obligatoria
—
—
Si
Si
Gerente de cuenta
dedicado
—
—
—
Si
Instancia y base de
datos dedicadas
—
—
—
Si
Acuerdo de nivel de
servicio
personalizado
—
—
—
Si


**Herramientas invocadas:**

1. `buscar_en_documentacion({'consulta': '¿Qué diferencia hay entre el plan Profesional y el Negocio?', 'top_k': 3})`

---

## 6. ¿Usan las conversaciones de mis clientes para entrenar modelos de IA?

**Modo demo (sin clave de API).** Extractos textuales de la documentación, sin redacción del modelo:

**1. FAQ de Soporte, pág. 4, sección «E3. ¿Pueden ver las conversaciones de mis clientes?»**

> E3. ¿Pueden ver las conversaciones de mis clientes?
Solo personal técnico autorizado, únicamente ante un ticket de soporte abierto por vos, y queda
registrado en un log de auditoría que podés solicitar. No usamos el contenido de tus
conversaciones para entrenar modelos.

**2. Política de Privacidad, pág. 2, sección «4. Uso de inteligencia artificial»**

> 4. Uso de inteligencia artificial
El bot conversacional de Brokitech Turnos utiliza modelos de lenguaje de terceros para interpretar
los mensajes de los Usuarios Finales.
•
Los mensajes se envían al proveedor del modelo únicamente para generar la respuesta de esa
conversación.
•
No usamos el contenido de las conversaciones de nuestros Clientes para entrenar ni afinar
modelos, ni propios ni de terceros.
•
Tenemos acuerdos con los proveedores que prohíben el uso de los datos enviados para
entrenamiento.
•
Antes de enviar un mensaje al modelo, aplicamos un filtro que enmascara números de tarjeta
y documentos de identidad si son detectados.
Un Cliente puede desactivar el procesamiento por IA desde Configuración -> Privacidad ->
Desactivar asistente IA. En ese caso el bot funciona con flujos guiados por menú, sin lenguaje
natural.

**3. FAQ de Soporte, pág. 2, sección «B3. El bot no responde a mis clientes. ¿Qué reviso?»**

> B3. El bot no responde a mis clientes. ¿Qué reviso?
En orden:


**Herramientas invocadas:**

1. `buscar_en_documentacion({'consulta': '¿Usan las conversaciones de mis clientes para entrenar modelos de IA?', 'top_k': 3})`

---

## 7. El bot dejó de responderle a mis clientes, ¿qué reviso?

**Modo demo (sin clave de API).** Extractos textuales de la documentación, sin redacción del modelo:

**1. FAQ de Soporte, pág. 2, sección «B3. El bot no responde a mis clientes. ¿Qué reviso?»**

> B3. El bot no responde a mis clientes. ¿Qué reviso?
En orden:

**2. FAQ de Soporte, pág. 4, sección «E3. ¿Pueden ver las conversaciones de mis clientes?»**

> E3. ¿Pueden ver las conversaciones de mis clientes?
Solo personal técnico autorizado, únicamente ante un ticket de soporte abierto por vos, y queda
registrado en un log de auditoría que podés solicitar. No usamos el contenido de tus
conversaciones para entrenar modelos.

**3. FAQ de Soporte, pág. 2, sección «B5. ¿Puedo intervenir manualmente una conversación?»**

> B5. ¿Puedo intervenir manualmente una conversación?
Sí. Desde Conversaciones podés tomar el control de cualquier chat con el botón Modo humano. El
bot deja de responder en ese chat durante 6 horas o hasta que lo devuelvas al modo automático.


**Herramientas invocadas:**

1. `buscar_en_documentacion({'consulta': 'El bot dejó de responderle a mis clientes, ¿qué reviso?', 'top_k': 3})`

---

## 8. ¿Se integra con AFIP para emitir factura electrónica automática?

**Modo demo (sin clave de API).** Extractos textuales de la documentación, sin redacción del modelo:

**1. FAQ de Soporte, pág. 1, sección «A5. ¿Emiten factura?»**

> A5. ¿Emiten factura?
Sí, factura tipo B o A según corresponda, emitida automáticamente y enviada por email dentro de
las 72 h de acreditado el pago. Cargá tu CUIT en Configuración -> Datos de facturación para
recibir factura A.

**2. Base de Conocimiento del Producto, pág. 1, sección «1.2 A quién NO está dirigido»**

> 1.2 A quién NO está dirigido
•
Negocios que venden productos físicos sin componente de turno (usar Brokitech CRM).
•
Empresas que necesitan facturación electrónica AFIP integrada (está en roadmap, no
disponible al día de hoy).
•
Operaciones fuera de Argentina. Al día de la fecha solo operamos con Mercado Pago Argentina
y números de WhatsApp con prefijo +54.

**3. Planes y Precios, pág. 3, sección «7. Facturación»**

> 7. Facturación
•
Ciclo mensual: se cobra el mismo día del mes de la fecha de alta.
•
Ciclo anual: un único pago por adelantado; se renueva automáticamente salvo cancelación.
•
Factura B o A (cargando CUIT) enviada por email dentro de las 72 h de acreditado el pago.
•
Medios: tarjeta de crédito, débito y débito automático por Mercado Pago. Transferencia
bancaria solo en Enterprise.


**Herramientas invocadas:**

1. `buscar_en_documentacion({'consulta': '¿Se integra con AFIP para emitir factura electrónica automática?', 'top_k': 3})`

---

## 9. ¿Cuál es la mejor receta de milanesas a la napolitana?

**Modo demo (sin clave de API).**

No encontré nada sobre eso en la documentación. Probá con otras palabras o escribí a soporte@brokitech.com.

**Herramientas invocadas:**

1. `buscar_en_documentacion({'consulta': '¿Cuál es la mejor receta de milanesas a la napolitana?', 'top_k': 3})`

---

## 10. Me cobraron dos veces el mes pasado y necesito que alguien lo revise.

**Modo demo (sin clave de API).** Extractos textuales de la documentación, sin redacción del modelo:

**1. Tabla comparativa de planes (CSV), pág. 1, sección «Plan Negocio»**

> Plan Negocio
plan: Negocio; precio mensual ars: 79900; precio anual por mes ars: 63920; ahorro anual ars: 191760; profesionales incluidos: 15; turnos por mes: ilimitados; servicios max: 200; conversaciones wa mes: 5000; usuarios panel: 25; analitica: si; google calendar: si; onboarding asistido: si; white label: si; api rest: si; webhooks: si; multi sucursal: si; sla contractual: 99.5%; soporte primera respuesta: 4 h habiles; costo profesional adicional ars: 3900; costo turno excedente ars: 0; costo conversacion excedente ars: 48; publico objetivo: Cadenas con sucursales clinicas y quienes necesitan API

**2. Planes y Precios, pág. 2, sección «4. Excedentes»**

> 4. Excedentes
Los planes tienen cupos. Superarlos no interrumpe el servicio; se factura el excedente en el ciclo
siguiente:
Concepto
Costo del excedente
Turno adicional (planes Inicial y Profesional)
$95 por turno
Conversación saliente adicional de WhatsApp
$48 por conversación
Profesional adicional (plan Profesional)
$4.900 por mes
Profesional adicional (plan Negocio)
$3.900 por mes
Sucursal adicional (plan Negocio)
$19.900 por mes
El plan Negocio no tiene límite de turnos, por lo que no genera excedente por ese concepto.
Enviamos un aviso por email al alcanzar el 80% y el 100% del cupo mensual.

**3. Términos y Condiciones de Uso, pág. 3, sección «8.1 Compensación por incumplimiento del SLA»**

> 8.1 Compensación por incumplimiento del SLA
Si en un mes calendario la disponibilidad cae por debajo del 99,5% en un plan con SLA, el Cliente
puede solicitar un crédito:
Disponibilidad mensual
Crédito sobre el abono del mes
99,0% – 99,49%
10%
95,0% – 98,99%
25%
Menos de 95,0%
50%
El crédito se solicita dentro de los 30 días, se aplica al ciclo siguiente y es el único remedio por
indisponibilidad.


**Herramientas invocadas:**

1. `buscar_en_documentacion({'consulta': 'Me cobraron dos veces el mes pasado y necesito que alguien lo revise.', 'top_k': 3})`

---
