from pathlib import Path
from uuid import uuid4


def make_artifacts_dir(base: Path) -> Path:
    """
    Crea /static/reports/{uuid}/ y retorna la ruta.
    """
    base.mkdir(parents=True, exist_ok=True)
    d = base / str(uuid4())
    d.mkdir(parents=True, exist_ok=True)
    return d
