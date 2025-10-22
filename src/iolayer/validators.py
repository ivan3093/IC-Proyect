from fastapi import UploadFile
from pathlib import Path
from src.utils.errors import ValidationError
#from ..utils.errors import ValidationError

ALLOWED_EXT = {".txt", ".TXT"}
ALLOWED_MIME = {"text/plain", "application/octet-stream"}
MAX_BYTES = 10 * 1024 * 1024  # 10 MB (adjustable)


def validate_txt_file(file: UploadFile, max_bytes: int = MAX_BYTES) -> None:
    """
    Validate .txt/.TXT extension, allowed MIME, and size (when available).
    Raise ValidationError if something doesn't comply.
    Reglas:
      Rules:
      - Required extension: .txt/.TXT
      - Allowed MIME: text/plain; application/octet-stream is allowed only if the extension is .txt
      - If content_type is not available, validate by extension
    """
    filename = file.filename or ""
    ext = Path(filename).suffix
    
    # 1) Required extension
    if ext not in ALLOWED_EXT:
    #if not filename.endswith(tuple(ALLOWED_EXT)):
        raise ValidationError("Only .txt files are allowed.")
    
    # 2) Lenient MIME (may not be set on some UploadFile instances)
    ct = getattr(file, "content_type", None)  # might not exist or be None
    if ct is not None:
        if ct not in ALLOWED_MIME:
            # Disallowed MIME
            raise ValidationError(f"Unsupported content-type: {ct}")
       # application/octet-stream is valid only if extension is .txt (already validated above)
        # if it were another extension, we wouldn't reach this point because we'd have failed above
   
   
   #if file.content_type not in ALLOWED_MIME:
        #raise ValidationError(f"Unsupported content-type: {file.content_type}")

    # Attempt to constrain size if the backend/proxy exposes it (not always available)
    # FastAPI/Starlette does not provide size directly; a real limit should be enforced at the server.
    # Here we just document the intention.
    # (Optional) read some bytes and reset the pointer if you enforce a hard limit in the app.
