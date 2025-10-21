import re
from typing import Iterable, Dict, List, Tuple, Optional
from src.utils.errors import FormatError, UnknownLevel

#PATTERN = r"^\s*\[(?i:INFO|WARNING|ERROR)\]\s*(.+?)\s*$"
#PATTERN = r"^\s*\[(INFO|WARNING|ERROR)\]\s*(.+?)\s*$"
#REGEX = re.compile(PATTERN, re.IGNORECASE)
REGEX = re.compile(r'^\s*\[(?P<level>[A-Za-z]+)\]\s*(?P<msg>.*?)\s*$', re.IGNORECASE)



ALLOWED_LEVELS = {"INFO", "WARNING", "ERROR"}


def parse_line(line: str, line_no: int) -> Tuple[str, str]:
    """
    Parsea una línea con formato: [LEVEL] Mensaje
    - Acepta minúsculas y espacios extra.
    - Normaliza LEVEL a MAYÚSCULAS.
    Returns:
        (level_upper, message_stripped)
    Raises:
        FormatError: si la línea no cumple el patrón.
        UnknownLevel: si el nivel no es INFO/WARNING/ERROR.
    """
    m = REGEX.match(line)
    if not m:
            # Formato incorrecto (ni siquiera corchetes/estructura)
        raise FormatError(line_no=line_no, line=line, last_ok_no=None, last_ok_line=None)

    #level_raw, message = m.group(1), m.group(2)
    level_raw = m.group("level")
    msg = m.group("msg")
    level = level_raw.upper() #Normalizes text to ALL CAPS  for level


    if level not in ALLOWED_LEVELS:
        # Estructura correcta, pero nivel NO permitido
        #raise UnknownLevel(line_no=line_no, line=line, last_ok_no=None, last_ok_line=None)
        err = UnknownLevel(line_no=line_no, line=line, last_ok_no=None, last_ok_line=None)
        raise err

    return level, msg


def log_analyzer(lines: Iterable[str]) -> Dict[str, List[str]]:
    """
    Itera línea a línea (streaming) y clasifica:
    Returns:
        {'ERROR': [...], 'WARNING': [...], 'INFO': [...]}
    Fail-fast:
        En primera línea inválida o nivel desconocido, lanza excepción con contexto.
    """
    result = {"ERROR": [], "WARNING": [], "INFO": []}

    last_ok_no: Optional[int] = None
    last_ok_line: Optional[str] = None

    for idx, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        try:
            level, msg = parse_line(line, idx)
            result[level].append(f"[{level}] {msg}")
            last_ok_no, last_ok_line = idx, f"[{level}] {msg}"
        except FormatError as e:
            # Enriquecer con última OK
            e.last_success_line_number = last_ok_no
            e.last_success_line_content = last_ok_line
            raise
        except UnknownLevel as e:
            e.last_success_line_number = last_ok_no
            e.last_success_line_content = last_ok_line
            raise

    return result
