import mimetypes
from pathlib import Path

from flask import Blueprint
from jinja2 import ChoiceLoader, FileSystemLoader

# ---------------------------------------------------------------------------
# Marca: PHPeitor Dataset (wordmark basado en el logo PHPEITOR de Bagisto)
# Los archivos viven en docker/branding (montado en /app/docker/branding) y se
# sirven en /branding/... para no depender de la imagen de Superset.
# ---------------------------------------------------------------------------
branding_bp = Blueprint(
    "phpeitor_branding",
    __name__,
    static_folder="/app/docker/branding",
    static_url_path="/branding",
)
BLUEPRINTS = [branding_bp]
BRANDING_DIR = Path("/app/docker/branding")

# El runtime de Rive necesita que el .wasm se sirva con su tipo MIME
mimetypes.add_type("application/wasm", ".wasm")


def brand_url(name):
    """URL de un archivo de marca con ?v=<fecha de modificación>.

    Superset cachea los estáticos hasta un año; al regenerar un archivo cambia la
    versión y el navegador descarga el nuevo.
    """
    try:
        version = int((BRANDING_DIR / name).stat().st_mtime)
    except OSError:
        version = 0
    return f"/branding/{name}?v={version}"


def FLASK_APP_MUTATOR(app):  # noqa: N802
    # Plantillas propias (docker/branding-templates) con prioridad sobre las de Superset
    app.jinja_loader = ChoiceLoader(
        [FileSystemLoader("/app/docker/branding-templates"), app.jinja_loader]
    )
    app.jinja_env.globals["brand_url"] = brand_url


APP_NAME = "PHPeitor Dataset"
APP_ICON = brand_url("phpeitor-dataset.svg")
LOGO_TARGET_PATH = "/dashboard/list/"
LOGO_TOOLTIP = "PHPeitor Dataset"
FAVICONS = [{"href": brand_url("favicon.svg"), "type": "image/svg+xml"}]

BABEL_DEFAULT_LOCALE = "es"

# Colores de la marca: azul marino #060C3B (principal) y rosa #f43f5e (acento)
THEME_OVERRIDES = {
    # ancho máx. del logo en la barra = gridUnit (4px) * brandIconMaxWidth
    "brandIconMaxWidth": 58,
    "colors": {
        "primary": {
            "base": "#060C3B",
            "dark1": "#04082A",
            "dark2": "#02051A",
            "light1": "#383D62",
            "light2": "#6A6D89",
            "light3": "#9B9DB1",
            "light4": "#CDCED8",
            "light5": "#E6E7EC",
        },
    },
}

EXTRA_CATEGORICAL_COLOR_SCHEMES = [
    {
        "id": "phpeitor",
        "description": "Colores de la marca PHPeitor Dataset",
        "label": "PHPeitor",
        "isDefault": True,
        "colors": [
            "#060C3B",
            "#F43F5E",
            "#3B4A9E",
            "#FB923C",
            "#0EA5E9",
            "#A3A3C2",
            "#BE123C",
            "#14B8A6",
        ],
    }
]

# CSP de producción de Superset 4.1.2 + 'wasm-unsafe-eval', que necesita el runtime
# de Rive (WebAssembly) en el login. En desarrollo se usa TALISMAN_DEV_CONFIG, que
# ya permite 'unsafe-eval'.
TALISMAN_CONFIG = {
    "content_security_policy": {
        "base-uri": ["'self'"],
        "default-src": ["'self'"],
        "img-src": [
            "'self'",
            "blob:",
            "data:",
            "https://apachesuperset.gateway.scarf.sh",
            "https://static.scarf.sh/",
        ],
        "worker-src": ["'self'", "blob:"],
        "connect-src": [
            "'self'",
            "https://api.mapbox.com",
            "https://events.mapbox.com",
        ],
        "object-src": "'none'",
        "style-src": [
            "'self'",
            "'unsafe-inline'",
        ],
        "script-src": ["'self'", "'strict-dynamic'", "'wasm-unsafe-eval'"],
    },
    "content_security_policy_nonce_in": ["script-src"],
    "force_https": False,
    "session_cookie_secure": False,
}
