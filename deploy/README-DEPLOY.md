# Publicar el agente en la nube

El proyecto no depende de ninguna nube en particular: es una app Streamlit que
lee PDF y CSV del propio repositorio. Abajo están las tres opciones probadas,
ordenadas por facilidad.

Los PDF se generan solos en el arranque a partir del Markdown versionado
(`src/ingest.py::asegurar_pdfs`), así que ninguna plataforma necesita un paso
de build manual.

---

## Opción A — Streamlit Community Cloud (recomendada)

Gratis, sin tarjeta de crédito, pensada exactamente para este tipo de app.

**Requisitos:** el repo tiene que ser público y tener `requirements.txt` en la raíz. Ya cumple ambos.

1. Entrá a **https://share.streamlit.io** e iniciá sesión con tu cuenta de GitHub.
2. **Create app → Deploy a public app from GitHub**.
3. Completá:
   | Campo | Valor |
   |---|---|
   | Repository | `brokitech-rgb/Challenge-Alura-Agente` |
   | Branch | `master` |
   | Main file path | `app.py` |
4. Antes de dar Deploy, abrí **Advanced settings → Secrets** y pegá:
   ```toml
   DEEPSEEK_API_KEY = "sk-tu-clave"
   ```
   Si lo dejás vacío la app igual levanta, en modo demo.
5. **Deploy**. El primer build tarda 2–4 minutos.

Queda publicada en `https://<nombre-que-elijas>.streamlit.app`

> Las apps gratuitas se suspenden tras varios días sin visitas y se reactivan
> solas con la primera visita. Si vas a mostrarla, entrá una vez antes.

---

## Opción B — Hugging Face Spaces

También gratis y sin tarjeta. Conviene si querés que el deploy no dependa de
Streamlit Cloud, o si preferís controlar la imagen con Docker.

1. Entrá a **https://huggingface.co/new-space**.
2. Configurá:
   | Campo | Valor |
   |---|---|
   | Space name | `agente-brokitech` |
   | License | MIT |
   | SDK | **Streamlit** |
   | Hardware | CPU basic (gratis) |
   | Visibility | Public |
3. En **Settings → Variables and secrets → New secret**, agregá
   `DEEPSEEK_API_KEY` con tu clave.
4. Subí el código:
   ```bash
   git remote add space https://huggingface.co/spaces/<tu-usuario>/agente-brokitech
   git push space master:main
   ```

El archivo `README-HF.md` de este directorio contiene el encabezado YAML que
Hugging Face necesita: copialo como `README.md` en la raíz del Space si el
build no arranca solo.

Queda en `https://huggingface.co/spaces/<tu-usuario>/agente-brokitech`

---

## Opción C — Oracle Cloud Infrastructure (OCI)

Si conseguís la cuenta de OCI, el despliegue en una VM del tier Always Free está
documentado paso a paso en **[README-OCI.md](README-OCI.md)**, con Dockerfile,
`docker-compose.yml`, unidad de systemd y configuración de nginx incluidas en
este mismo directorio.

---

## Cualquier host con Docker

Los archivos de `deploy/` no son específicos de OCI. Sirven igual en Render,
Railway, Fly.io, una VPS o tu propia máquina:

```bash
docker compose -f deploy/docker-compose.yml up -d --build
```

La app queda en `http://localhost:8501`.

---

## Verificación posterior al deploy

Una vez publicada, comprobá que:

- [ ] La barra lateral muestra **6 documentos** y **124 fragmentos** indexados.
- [ ] Si cargaste la clave, dice *"Modelo activo: deepseek-chat"* y no *"Modo demo"*.
- [ ] Una pregunta del listado sugerido devuelve respuesta **con cita de fuente**.
- [ ] El desplegable *"Razonamiento"* muestra las llamadas a herramientas.
- [ ] Preguntar algo fuera de dominio ("receta de milanesas") devuelve que no
      está en la documentación, en lugar de inventar.
