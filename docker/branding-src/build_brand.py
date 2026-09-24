"""Genera los archivos de marca PHPeitor Dataset.

Uso:  python3 docker/branding-src/build_brand.py

Salidas:
  docker/branding/phpeitor-dataset.svg              logo de la barra (con animación)
  docker/branding/favicon.svg                       favicon
  docker/branding-templates/_phpeitor_footer.html   footer (SVG en línea, estilo Bagisto)

El wordmark PHPEITOR es el del proyecto Bagisto (brand-logo.blade.php). Las letras
de DATASET se construyen con la misma geometría: trazos de 28, barras de 27.51,
ranuras de 8.25 e inclinación de 22.993 por cada 99.035 de alto.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAVY, ROSE, CREAM = "#060C3B", "#F43F5E", "#F1EADF"

H = 99.035
K = 22.993 / H
B1, B2, B3, B4 = 27.510, 35.763, 63.272, 71.525
PHPEITOR = "M16.607 27.510L22.994 0.000L108.175 0.000L93.484 63.272L36.697 63.272L28.394 99.035L0.000 99.035L14.690 35.763L71.478 35.763L73.394 27.510Z M124.175 0.000H152.175L129.182 99.035H101.182Z M196.175 0.000H224.175L201.182 99.035H173.182Z M115.929 35.517H215.929L209.428 63.517H109.428Z M256.782 27.510L263.169 0.000L348.350 0.000L333.659 63.272L276.872 63.272L268.569 99.035L240.175 99.035L254.865 35.763L311.653 35.763L313.569 27.510Z M472.525 0.000L387.344 0.000L380.957 27.510L466.138 27.510Z M447.185 35.763L379.040 35.763L372.653 63.273L440.798 63.273Z M455.919 71.525L370.737 71.525L364.350 99.035L449.531 99.035Z M488.525 0.000H516.525L493.532 99.035H465.532Z M532.525 0.000H632.525L626.024 28.000H526.024Z M568.525 0.000H596.525L573.532 99.035H545.532Z M648.525 0.000H764.525L758.024 28.000H642.024Z M632.033 71.035H748.033L741.532 99.035H625.532Z M648.525 0.000H676.525L653.532 99.035H625.532Z M736.525 0.000H764.525L741.532 99.035H713.532Z M797.132 27.510L803.519 0.000L888.700 0.000L874.009 63.272L817.222 63.272L808.919 99.035L780.525 99.035L795.215 35.763L852.003 35.763L853.919 27.510Z M840.525 50.000L868.525 50.000L896.525 99.035L868.525 99.035Z"
PHPEITOR_W = 896.525

# Glifos en coordenadas rectas (y=0 arriba, y=H base): (ancho, [polígonos])
# Los huecos van en sentido inverso para que se rellenen bien con fill-rule nonzero.
GLYPHS = {
    "D": (100, [[(0, 0), (72, 0), (100, 28), (100, 71.035), (72, H), (0, H)],
                [(28, 28), (28, 71.035), (72, 71.035), (72, 28)]]),
    "A": (100, [[(0, 0), (100, 0), (100, H), (72, H), (72, B3), (28, B3), (28, H), (0, H)],
                [(28, B1), (28, B2), (72, B2), (72, B1)]]),
    "T": (100, [[(0, 0), (100, 0), (100, 28), (64, 28), (64, H), (36, H), (36, 28), (0, 28)]]),
    "S": (85.181, [[(0, 0), (85.181, 0), (85.181, B1), (28.394, B1), (28.394, B2),
                    (85.181, B2), (85.181, H), (0, H), (0, B4), (56.787, B4),
                    (56.787, B3), (0, B3)]]),
    "E": (85.181, [[(0, 0), (85.181, 0), (85.181, B1), (0, B1)],
                   [(0, B2), (68.145, B2), (68.145, B3), (0, B3)],
                   [(0, B4), (85.181, B4), (85.181, H), (0, H)]]),
}


def word(text, scale, gap):
    """Devuelve (path, ancho) de una palabra con origen en (0, 0)."""
    parts, x = [], 0.0
    for ch in text:
        w, polys = GLYPHS[ch]
        for poly in polys:
            pts = [(x + scale * px + K * scale * (H - py), scale * py) for px, py in poly]
            parts.append("M" + "L".join(f"{a:.3f} {b:.3f}" for a, b in pts) + "Z")
        x += scale * w + gap
    return " ".join(parts), x - gap


# DATASET pequeño, compacto y alineado a la derecha bajo PHPEITOR
TAG_SCALE, TAG_GAP, TAG_TOP = 0.25, 9, H + 16
TAG, tag_w = word("DATASET", TAG_SCALE, TAG_GAP)
TAG_X = PHPEITOR_W - tag_w  # base de la última T alineada con la pata de la R
LOCKUP_H = TAG_TOP + TAG_SCALE * H
VIEWBOX = f"-6 -4 908 {LOCKUP_H + 8:.0f}"


def trace_css(width, glow):
    return f"""
    .phpeitor-trace {{
      fill: none; stroke: {ROSE}; stroke-opacity: 1; stroke-width: {width};
      stroke-dasharray: 70 200; vector-effect: non-scaling-stroke;
      filter: drop-shadow(0 0 {glow}px {ROSE}) drop-shadow(0 0 1px #fff);
      animation: phpeitor-trace 5s linear infinite;
    }}
    @keyframes phpeitor-trace {{ to {{ stroke-dashoffset: -270px; }} }}
    @media (prefers-reduced-motion: reduce) {{ .phpeitor-trace {{ display: none; }} }}"""


def lockup_svg(uid, extra_attrs="", style=""):
    style_tag = f"<style>{style}\n  </style>" if style else ""
    return f"""<svg {extra_attrs}viewBox="{VIEWBOX}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="PHPeitor Dataset">
  <title>PHPeitor Dataset</title>
  {style_tag}
  <defs>
    <path id="{uid}" d="{PHPEITOR}"/>
  </defs>
  <use href="#{uid}" fill="{NAVY}"/>
  <path transform="translate({TAG_X:.3f} {TAG_TOP:.3f})" fill="{ROSE}" d="{TAG}"/>
  <use href="#{uid}" class="phpeitor-trace"/>
</svg>
"""


def main():
    brand = ROOT / "branding"
    templates = ROOT / "branding-templates"
    brand.mkdir(exist_ok=True)
    templates.mkdir(exist_ok=True)

    (brand / "phpeitor-dataset.svg").write_text(
        lockup_svg("phpeitor-wordmark", style=trace_css(1.5, 3))
    )

    p_glyph = PHPEITOR.split("Z")[0] + "Z"
    (brand / "favicon.svg").write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="-8 -8 124 116">
  <style>{trace_css(1.5, 2)}
  </style>
  <rect x="-8" y="-8" width="124" height="116" rx="22" fill="{CREAM}"/>
  <path id="p" d="{p_glyph}" fill="{NAVY}"/>
  <use href="#p" class="phpeitor-trace"/>
</svg>
"""
    )

    (templates / "_phpeitor_footer.html").write_text(
        "{# Generado por docker/branding-src/build_brand.py: no editar a mano #}\n"
        + lockup_svg("phpeitor-footer-wordmark", 'class="phpeitor-logo" ')
    )


if __name__ == "__main__":
    main()
