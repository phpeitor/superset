from flask import Blueprint
from jinja2 import ChoiceLoader, FileSystemLoader

PUBLIC_ROLE_LIKE = "Gamma"

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


def FLASK_APP_MUTATOR(app):  # noqa: N802
    # Plantillas propias (docker/branding-templates) con prioridad sobre las de Superset
    app.jinja_loader = ChoiceLoader(
        [FileSystemLoader("/app/docker/branding-templates"), app.jinja_loader]
    )


APP_NAME = "PHPeitor Dataset"
APP_ICON = "/branding/phpeitor-dataset.svg"
LOGO_TARGET_PATH = "/dashboard/list/"
LOGO_TOOLTIP = "PHPeitor Dataset"
FAVICONS = [{"href": "/branding/favicon.svg", "type": "image/svg+xml"}]

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
