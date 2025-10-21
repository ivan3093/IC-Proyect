from fastapi import UploadFile
from pathlib import Path
from src.utils.errors import ValidationError
#from ..utils.errors import ValidationError

ALLOWED_EXT = {".txt", ".TXT"}
ALLOWED_MIME = {"text/plain", "application/octet-stream"}
MAX_BYTES = 10 * 1024 * 1024  # 10 MB (ajustable)


def validate_txt_file(file: UploadFile, max_bytes: int = MAX_BYTES) -> None:
    """
    Valida extensión .txt/.TXT, MIME permitido y tamaño (cuando esté disponible).
    Lanza ValidationError si algo no cumple.
    Reglas:
      - Extensión obligatoria .txt/.TXT
      - MIME permitido: text/plain; application/octet-stream se permite solo si la extensión es .txt
      - Si content_type no está disponible, validamos por extensión
    """
    filename = file.filename or ""
    ext = Path(filename).suffix
    
    # 1) Extensión obligatoria
    if ext not in ALLOWED_EXT:
    #if not filename.endswith(tuple(ALLOWED_EXT)):
        raise ValidationError("Only .txt files are allowed.")
    
    # 2) MIME tolerante (puede no venir seteado en algunos UploadFile)
    ct = getattr(file, "content_type", None)  # podría no existir o ser None
    if ct is not None:
        if ct not in ALLOWED_MIME:
            # MIME no permitido
            raise ValidationError(f"Unsupported content-type: {ct}")
        # application/octet-stream solo es válido si extensión es .txt (ya validada)
        # si fuera otra ext (no llega aquí porque ya habríamos fallado arriba)
   
   
   #if file.content_type not in ALLOWED_MIME:
        #raise ValidationError(f"Unsupported content-type: {file.content_type}")

    # Intento acotar tamaño si el backend/proxy lo expone (no siempre disponible)
    # FastAPI/Starlette no da el tamaño directo; límite real se debe configurar en servidor
    # Aquí solo documentamos la intención.
    # (Opcional) leer algunos bytes y reposicionar puntero si se fija un límite duro en app.
