# PHPeitor Dataset: despliegue en un servidor nuevo

Superset 4.1.2 (imagen oficial) con la marca PHPeitor Dataset aplicada solo por
configuración, sin recompilar el frontend.

## Requisitos
- Docker con el plugin `docker compose`.

## Pasos
```bash
git clone https://github.com/phpeitor/superset.git
cd superset

# 1. Variables propias (no están en git)
cp .env.example .env                  # TAG de la imagen
cat > docker/.env-local <<X
SUPERSET_SECRET_KEY=$(openssl rand -base64 42)
X
# docker/.env-local sobrescribe los valores de ejemplo de docker/.env
# (contraseñas de Postgres, SECRET_KEY, etc.). También está en .gitignore.

# 2. Levantar
docker compose -f docker-compose-image-tag.yml up -d
```
Superset queda en el puerto definido en `docker-compose-image-tag.yml`.
`docker/requirements-local.txt` instala los drivers `pymssql` (SQL Server) y
`pymysql` al arrancar.

## Dónde está la marca
| Archivo | Qué hace |
|---|---|
| `docker/pythonpath_dev/superset_config_docker.py` | Nombre, logo, favicon, idioma, colores del tema, paleta de gráficos, rutas `/branding` y plantillas propias |
| `docker/branding/` | Logo (`phpeitor-dataset.svg`), favicon, personaje del login (`dataset.riv`) y runtime de Rive (`rive/`), servidos en `/branding/...` |
| `docker/branding-templates/tail_js_custom_extra.html` | Colores de login y formularios |
| `docker/branding-templates/appbuilder/general/security/login_db.html` | Login con el personaje Rive: Typing al escribir, cargando al enviar, Correct/Wrong según el resultado, Jump al hacer clic |
| `docker/branding-src/build_brand.py` | Genera los SVG y el footer (`python3 docker/branding-src/build_brand.py`) |

Después de cambiar la configuración o regenerar el logo: `docker restart superset_app`.
Las URLs de marca llevan `?v=<fecha del archivo>`, así que el navegador descarga la versión nueva sin limpiar caché.

## Qué no viaja en git
- `.env` y `docker/.env-local`: llaves y contraseñas.
- La base de metadatos (dashboards, charts, conexiones): se exporta desde
  Superset (*Dashboards → Exportar*) o con un respaldo del volumen de Postgres
  `superset_db_home`.
