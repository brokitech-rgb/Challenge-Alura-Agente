# Deploy en Oracle Cloud Infrastructure (OCI)

Guía reproducible para publicar el agente en una VM del tier **Always Free** de OCI.

---

## 1. Crear la instancia

En la consola de OCI: **Compute → Instances → Create instance**.

| Campo | Valor |
|---|---|
| Nombre | `agente-brokitech` |
| Imagen | Canonical Ubuntu 24.04 |
| Shape | `VM.Standard.A1.Flex` — 1 OCPU, 6 GB RAM (Always Free) |
| VCN | Crear una nueva con subnet pública |
| Asignar IP pública | Sí |
| Clave SSH | Subí tu clave pública |

> La shape `A1.Flex` es ARM (Ampere). La imagen `python:3.12-slim` del Dockerfile
> es multi-arquitectura, así que funciona sin cambios. Si te aparece
> *"Out of host capacity"*, probá otro Availability Domain o usá la shape
> `VM.Standard.E2.1.Micro` (x86, también Always Free).

Anotá la **IP pública** que te asigna OCI.

---

## 2. Abrir el puerto 8501

Son **dos** reglas, y olvidarse de la segunda es el error más común.

### 2.1 Security List (firewall de la red virtual)

**Networking → Virtual Cloud Networks → tu VCN → Security Lists → Default Security List → Add Ingress Rules**

| Campo | Valor |
|---|---|
| Stateless | No |
| Source CIDR | `0.0.0.0/0` |
| IP Protocol | TCP |
| Destination Port Range | `8501` |

### 2.2 Firewall del sistema operativo

Ubuntu en OCI viene con `iptables` cerrado por defecto:

```bash
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8501 -j ACCEPT
sudo netfilter-persistent save
```

---

## 3. Preparar la VM

```bash
ssh -i ~/.ssh/tu-clave ubuntu@<IP_PUBLICA>
```

```bash
sudo apt update && sudo apt install -y docker.io docker-compose-v2 git
sudo usermod -aG docker $USER && newgrp docker
```

---

## 4. Desplegar

```bash
git clone https://github.com/brokitech-rgb/Challenge-Alura-Agente.git
cd Challenge-Alura-Agente
```

Cargá la clave del modelo (si la omitís, la app arranca igual en modo demo):

```bash
printf 'DEEPSEEK_API_KEY=sk-tu-clave\n' > .env
```

```bash
docker compose -f deploy/docker-compose.yml --env-file .env up -d --build
```

Verificar:

```bash
docker compose -f deploy/docker-compose.yml ps
curl -s http://localhost:8501/_stcore/health
```

La app queda en **http://\<IP_PUBLICA\>:8501**

---

## 5. Alternativa sin Docker (systemd)

Si preferís correr directo sobre la VM:

```bash
sudo apt install -y python3-venv
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
./.venv/bin/python scripts/build_pdfs.py
sudo cp deploy/agente-brokitech.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now agente-brokitech
sudo systemctl status agente-brokitech
```

---

## 6. HTTPS con dominio propio (opcional)

```bash
sudo apt install -y nginx certbot python3-certbot-nginx
sudo cp deploy/nginx-agente.conf /etc/nginx/sites-available/agente
sudo ln -s /etc/nginx/sites-available/agente /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d agente.tudominio.com
```

Acordate de abrir también los puertos 80 y 443 en la Security List.

---

## 7. Operación

```bash
# Ver logs en vivo
docker compose -f deploy/docker-compose.yml logs -f

# Reiniciar
docker compose -f deploy/docker-compose.yml restart

# Actualizar tras un push al repo
git pull && docker compose -f deploy/docker-compose.yml up -d --build

# Detener
docker compose -f deploy/docker-compose.yml down
```

---

## 8. Diagnóstico

| Síntoma | Causa habitual |
|---|---|
| La página no carga desde afuera | Falta la regla de Ingress, o falta abrir `iptables` en la VM |
| `curl localhost:8501` funciona pero la IP pública no | Es lo anterior: el contenedor está bien, la red no |
| El contenedor reinicia en loop | `docker compose logs` — casi siempre falta memoria en shapes Micro |
| Responde en "modo demo" | No se cargó `DEEPSEEK_API_KEY` en el `.env` |
| `No hay PDF en docs/pdf` | Correr `python scripts/build_pdfs.py` (el Dockerfile ya lo hace solo) |
