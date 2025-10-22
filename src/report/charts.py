from pathlib import Path
from typing import Dict
#import matplotlib.pyplot as plt


def build_bar_chart_png(counts: Dict[str, int], out_dir: Path, filename: str = "severity.png") -> Path:
    """
    Genera una gráfica de barras (ERROR/WARNING/INFO) y guarda PNG en out_dir.
    No especifica colores ni estilos (simple).
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / filename

    try:
        import matplotlib.pyplot as plt  # <-- lazy import
        labels = ["ERROR", "WARNING", "INFO"]
        values = [counts.get(k, 0) for k in labels]

        # Gráfica simple
        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_title("Logs by severity")
        ax.set_ylabel("Count")
        ax.set_xlabel("Severity")
        fig.tight_layout()
        fig.savefig(path)
        plt.close(fig)
    except Exception as e:
        # Fallback: crea un PNG vacío o un texto como placeholder
        # Para simplicidad, un archivo mínimo:
        path.write_bytes(b"")  # o podrías escribir una imagen pre-generada
        # (Opcional) loggear e.info para que quede rastro
        # print(f"[WARN] Chart not generated: {e}")

    return path
