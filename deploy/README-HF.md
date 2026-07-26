---
title: Agente de Soporte Brokitech Turnos
emoji: 📅
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.60.0
app_file: app.py
pinned: false
license: mit
short_description: Agente RAG que responde sobre la documentación de un SaaS de turnos
---

# Agente de Soporte — Brokitech Turnos

Agente de IA que responde consultas de soporte a partir de cinco documentos PDF
y un CSV: base de conocimiento, FAQ, política de privacidad, planes y precios, y
términos de uso.

Para que responda con el modelo de lenguaje, cargá el secreto `GROQ_API_KEY`
en **Settings → Variables and secrets**. Sin él, la app funciona en modo demo y
devuelve extractos textuales recuperados de los PDF.

Código y documentación completa: https://github.com/brokitech-rgb/Challenge-Alura-Agente
