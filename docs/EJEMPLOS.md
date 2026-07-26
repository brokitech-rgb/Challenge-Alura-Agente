# Ejemplos de preguntas y respuestas

> Archivo generado por `python scripts/generar_ejemplos.py`. 
> Las respuestas son la salida textual del agente, sin editar.

- **Generado:** 26/07/2026 14:26
- **Motor:** modelo `openai/gpt-oss-120b`
- **Fragmentos indexados:** 124

---

## 1. ¿Brokitech se queda con una parte de la seña que cobro?

No, Brokitech no se queda con ninguna parte de la seña que cobras. El 100 % de la seña se transfiere a tu cuenta de Mercado Pago; nuestro único cobro es el abono mensual del plan, y la única deducción que puede existir es la comisión que cobra Mercado Pago, que no es nuestra.

Fuente: FAQ de Soporte, pág. 2

**Herramientas invocadas:**

1. `buscar_en_documentacion({'consulta': 'seña cobro retención Brokitech'})`

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

> Aviso: Falló la llamada al modelo (Error code: 400 - {'error': {'message': 'Tool call validation failed: tool call validation failed: parameters for tool consultar_planes did not match schema: errors: [`/plan`: expected string, but got null]', 'type': 'invalid_request_error', 'code': 'tool_use_failed', 'failed_generation': '{"name": "consultar_planes", "arguments": {\n  "plan": null\n}}'}}). Se respondió con extractos.

---

## 3. ¿Puedo usar mi número actual de WhatsApp Business?

Sí, podés usar tu número actual, pero **tenés que liberarlo de WhatsApp Business antes de conectarlo a la Cloud API**.  

**Cómo hacerlo**

1. En la app de WhatsApp Business, entrá a **Configuración → Cuenta → Eliminar mi cuenta**.  
2. Esperá unos minutos (el número queda libre).  
3. Conectá el número a Brokitech Turnos mediante la Cloud API.  

Tenés en cuenta que:

- **Perderás el historial de chats** previo al borrado.  
- La mayoría de los clientes prefieren crear una línea nueva y dedicada para evitar interrupciones.  

Fuentes:  
- FAQ de Soporte, pág. 2, sección «B1. ¿Puedo usar mi número actual de WhatsApp Business?».  
- Base de Conocimiento del Producto, pág. 3, sección «4.1 Qué número se puede usar».

**Herramientas invocadas:**

1. `buscar_en_documentacion({'consulta': 'usar número actual de WhatsApp Business con Brokitech Turnos'})`

---

## 4. Si cancelo la suscripción, ¿cuánto tiempo tengo para exportar mis datos?

Tenés **60 días** desde que cancelás la suscripción para exportar tus datos. Durante ese período la cuenta queda en modo lectura y podés descargar un ZIP con todos los CSV (clientes, turnos, pagos y servicios). Pasados los 60 días los datos se eliminan de forma permanente.  

Fuente: FAQ de Soporte, pág. 1, sección «A4. ¿Qué pasa con mis datos si cancelo?».  
Fuente: FAQ de Soporte, pág. 4, sección «E5. ¿Puedo exportar todos mis datos?».

**Herramientas invocadas:**

1. `buscar_en_documentacion({'consulta': 'tiempo para exportar datos después de cancelar suscripción'})`

---

## 5. ¿Qué diferencia hay entre el plan Profesional y el Negocio?

**Respuesta breve**  
El plan **Negocio** es la versión ampliada del plan **Profesional**: cuesta más, incluye más profesionales, turnos ilimitados y funcionalidades avanzadas (white‑label, API REST, webhooks, sucursales múltiples, SLA 99,5 % y soporte con primera respuesta en 4 h). El plan **Profesional** tiene un límite de 800 turnos/mes, 5 profesionales incluidos y no incluye esas herramientas avanzadas.

**Detalle comparativo**

| Característica | Plan Profesional | Plan Negocio |
|----------------|------------------|--------------|
| Precio mensual (IVA incl.) | $39 900 | $79 900 |
| Precio anual (mes promedio) | $31 920 | $63 920 |
| Ahorro anual | $95 760 | $191 760 |
| Profesionales incluidos | 5 | 15 |
| Turnos por mes | 800 (excedente $95/turno) | Ilimitados (sin costo de excedente) |
| Conversaciones WhatsApp/mes | 1 500 (excedente $48) | 5 000 (excedente $48) |
| Usuarios panel | 8 | 25 |
| Analítica | Sí | Sí |
| Google Calendar | Sí | Sí |
| Onboarding asistido | Sí | Sí |
| White‑label | No | Sí |
| API REST | No | Sí |
| Webhooks | No | Sí |
| Multi‑sucursal | No | Sí |
| SLA contractual | No | 99,5 % |
| Soporte (primera respuesta) | ≤ 24 h hábiles (email + WhatsApp) | ≤ 4 h hábiles (email + WhatsApp + teléfono) |
| Público objetivo | Peluquerías y centros de estética de 2‑5 personas | Cadenas con sucursales, clínicas o quien necesite API y marca propia |

**Fuentes**  
Fuente: Tabla comparativa de planes (CSV), pág. 1, sección «Plan Profesional»  
Fuente: Tabla comparativa de planes (CSV), pág. 1, sección «Plan Negocio»  
Fuente: Planes y Precios, pág. 2, sección «4. Excedentes»  
Fuente: FAQ de Soporte, pág. 4, sección «G. Tiempos de respuesta del soporte»  
Fuente: Planes y Precios, pág. 4, sección «8. Cómo elegir plan»

**Herramientas invocadas:**

1. `buscar_en_documentacion({'consulta': 'diferencias entre plan Profesional y plan Negocio'})`

---

## 6. ¿Usan las conversaciones de mis clientes para entrenar modelos de IA?

No. El contenido de las conversaciones de tus clientes **no se usa** para entrenar ni afinar modelos de IA, ni propios ni de terceros.

**Detalle**

- Sólo el personal técnico autorizado puede acceder a los mensajes, y solo cuando hay un ticket de soporte abierto por vos, quedando registrado en un log de auditoría que podés solicitar.  
- La Política de Privacidad indica explícitamente que los mensajes se envían al proveedor del modelo únicamente para generar la respuesta de esa conversación y que **no se utilizan** para entrenamiento. Además, tenés la opción de desactivar el procesamiento por IA desde *Configuración → Privacidad → Desactivar asistente IA*.  

Fuentes:  
- FAQ de Soporte, pág. 4, sección «E3. ¿Pueden ver las conversaciones de mis clientes?».  
- Política de Privacidad, pág. 2, sección «4. Uso de inteligencia artificial».

**Herramientas invocadas:**

1. `buscar_en_documentacion({'consulta': 'uso de conversaciones de clientes para entrenar modelos de IA'})`

---

## 7. El bot dejó de responderle a mis clientes, ¿qué reviso?

**Qué revisá cuando el bot no responde a tus clientes**

1. **Credenciales y acceso**  
   - Verificá que la cuenta y la API de WhatsApp estén activas y con credenciales correctas.  

2. **Configuración del bot**  
   - Confirmá que el flujo de conversación esté habilitado y que no haya sido puesto en modo “humano” accidentalmente.  

3. **Límites de la API de WhatsApp**  
   - Revisá que no hayas superado los límites de mensajes o que la cuenta no esté bloqueada por Meta.  

4. **Estado de los servicios de terceros**  
   - Chequeá si hay incidencias en WhatsApp Cloud API, Mercado Pago o en la infraestructura de Brokitech (pueden afectar la entrega de mensajes).  

5. **Modo manual**  
   - Si en alguna conversación activaste “Modo humano”, el bot deja de responder durante 6 h o hasta que lo vuelvas a cambiar a automático.  

6. **Logs y alertas**  
   - Revisá los logs de la plataforma (en la sección “Conversaciones”) para identificar errores o rechazos de entrega.  

Si después de revisar todo lo anterior el problema persiste, podés escalar a soporte para que investiguemos con más detalle.

Fuente: FAQ de Soporte, pág. 2, sección «B3. El bot no responde a mis clientes. ¿Qué reviso?».

**Herramientas invocadas:**

1. `buscar_en_documentacion({'consulta': 'bot no responde clientes troubleshooting'})`

---

## 8. ¿Se integra con AFIP para emitir factura electrónica automática?

No, todavía no hay integración con la AFIP para generar facturas electrónicas de forma automática. La integración de facturación AFIP está en roadmap y se espera para el Q4 2026【Base de Conocimiento del Producto, pág. 3, sección «5. Integraciones disponibles»】.  

En la actualidad el sistema sí emite facturas tipo A o B de forma automática y las envía por email dentro de las 72 h posteriores al pago, pero la generación directa a través de la AFIP no está disponible todavía【FAQ de Soporte, pág. 1, sección «A5. ¿Emiten factura?»】.

**Herramientas invocadas:**

1. `buscar_en_documentacion({'consulta': 'integración con AFIP factura electrónica automática'})`

---

## 9. ¿Cuál es la mejor receta de milanesas a la napolitana?

Eso no está cubierto en la documentación que tengo. ¿Querés que lo escale a soporte humano?

---

## 10. Me cobraron dos veces el mes pasado y necesito que alguien lo revise.

Se generó un ticket de soporte para que revisemos el cobro duplicado del mes pasado.

- **Ticket:** BTK-0001  
- **Motivo:** Facturación  
- **Canal de contacto:** soporte@brokitech.com / WhatsApp +54 9 11 5555‑0143  

Nuestro equipo de facturación lo revisará y se pondrá en contacto a la brevedad. Si tenés algún dato adicional (por ejemplo, número de factura o captura del cobro), podés enviarlo respondiendo a este mensaje.  

¡Gracias por avisarnos!  

Fuente: Sistema interno de tickets.

**Herramientas invocadas:**

1. `escalar_a_humano({'motivo': 'facturación', 'resumen': 'El usuario indica que le cobraron dos veces el mes pasado y solicita revisión.'})`

---
