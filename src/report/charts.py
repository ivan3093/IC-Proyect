from pathlib import Path
from typing import Dict
import matplotlib.pyplot as plt


def build_bar_chart_png(counts: Dict[str, int], out_dir: Path, filename: str = "severity.png") -> Path:
    """
    Genera una gráfica de barras (ERROR/WARNING/INFO) y guarda PNG en out_dir.
    No especifica colores ni estilos (simple).
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / filename

    labels = ["ERROR", "WARNING", "INFO"]
    values = [counts.get(k, 0) for k in labels]

    # Gráfica simple
    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_title("Logs por severidad")
    ax.set_ylabel("Conteo")
    ax.set_xlabel("Severidad")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)

    return path
