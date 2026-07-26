# Imagen del agente de soporte de Brokitech Turnos.
# Construir desde la RAÍZ del repositorio:
#   docker build -f deploy/Dockerfile -t agente-brokitech .
#
# python:3.12-slim funciona tal cual en las VM Ampere (ARM64) del tier
# Always Free de OCI: la imagen es multi-arquitectura.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Las dependencias van primero para que la capa quede cacheada entre builds.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY scripts/ ./scripts/
COPY docs/ ./docs/
COPY data/ ./data/
COPY app.py cli.py ./

# Los PDF se regeneran en la imagen a partir del Markdown versionado, así que
# el contenedor nunca depende de artefactos construidos en otra máquina.
RUN python scripts/build_pdfs.py

# Streamlit escribe métricas y config en el home del usuario.
RUN useradd --create-home --shell /bin/bash agente && chown -R agente:agente /app
USER agente

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')"

CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
