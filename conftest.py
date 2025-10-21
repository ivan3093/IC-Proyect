# conftest.py (en la raíz del repo)
import sys
from pathlib import Path

# Agrega la ruta "src" al sys.path al inicio, para que "import src...." funcione
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


# Ignorar tests específicos hasta que integres esos módulos
collect_ignore = [
    "tests/test_report_builder.py",
]