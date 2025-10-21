from pathlib import Path
from typing import Dict, List
from jinja2 import Environment, FileSystemLoader, select_autoescape


def build_report_html(
    result: Dict[str, List[str]],
    metrics: Dict,
    out_dir: Path,
    template_path: Path,
    samples: Dict[str, Dict[str, List[str]]] = None,  # <-- nuevo
) -> Path:
    """
    Renderiza un HTML Jinja2 con:
      - Totales y % por severidad
      - Top ERROR/WARNING
      - Imagen de barras (severity.png)
      - Muestras (primeras/últimas) opcionalmente
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(template_path.name)

    html = template.render(
        metrics=metrics,
        result=result,
        samples=samples or {"ERROR": {"first": [], "last": []},
                           "WARNING": {"first": [], "last": []},
                           "INFO": {"first": [], "last": []}},
        chart_filename="severity.png",
    )

    out_file = out_dir / "report.html"
    out_file.write_text(html, encoding="utf-8")
    return out_file
