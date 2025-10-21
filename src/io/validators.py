from fastapi import UploadFile
from src.utils.errors import ValidationError
#from ..utils.errors import ValidationError

ALLOWED_EXT = {".txt", ".TXT"}
ALLOWED_MIME = {"text/plain", "application/octet-stream"}
MAX_BYTES = 10 * 1024 * 1024  # 10 MB (ajustable)


def validate_txt_file(file: UploadFile, max_bytes: int = MAX_BYTES) -> None:
    """
    Valida extensión .txt/.TXT, MIME permitido y tamaño (cuando esté disponible).
    Lanza ValidationError si algo no cumple.
    """
    filename = file.filename or ""
    if not filename.endswith(tuple(ALLOWED_EXT)):
        raise ValidationError("Only .txt files are allowed.")

    if file.content_type not in ALLOWED_MIME:
        raise ValidationError(f"Unsupported content-type: {file.content_type}")

    # Intento acotar tamaño si el backend/proxy lo expone (no siempre disponible)
    # FastAPI/Starlette no da el tamaño directo; límite real se debe configurar en servidor
    # Aquí solo documentamos la intención.
    # (Opcional) leer algunos bytes y reposicionar puntero si se fija un límite duro en app.
