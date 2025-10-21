import io
import pytest
from starlette.datastructures import UploadFile
from src.iolayer.validators import validate_txt_file
from src.utils.errors import ValidationError


def _uf(name: str, content_type: str = "text/plain", data: bytes = b"x"):
    # NO pasamos content_type al constructor (para evitar TypeError en tu versión)
    uf = UploadFile(filename=name, file=io.BytesIO(data))
    # Intentamos asignarlo después; si no se puede, el validador usará la extensión
    try:
        uf.content_type = content_type
    except Exception:
        pass
    return uf
    #return UploadFile(filename=name, file=io.BytesIO(data), content_type=content_type)


def test_validate_txt_ok():
    f = _uf("a.txt", content_type="text/plain")
    validate_txt_file(f)  # no lanza


def test_validate_txt_wrong_ext():
    f = _uf("a.log", content_type="text/plain")
    with pytest.raises(ValidationError):
        validate_txt_file(f)


def test_validate_txt_bad_mime_but_allowed_ext():
    # application/octet-stream debe ser aceptado si la extensión es .txt
    f = _uf("a.txt", content_type="application/octet-stream")
    validate_txt_file(f)  # permitido por política


def test_validate_txt_bad_mime_and_ext():
    # Aunque sea octet-stream, con ext incorrecta debe fallar por la regla de extensión
    f = _uf("a.log", content_type="application/octet-stream")
    with pytest.raises(ValidationError):
        validate_txt_file(f)
