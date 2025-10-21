from pathlib import Path
from src.utils.files import make_artifacts_dir


def test_make_artifacts_dir(tmp_path):
    base = tmp_path / "static" / "reports"
    d = make_artifacts_dir(base)
    assert d.exists()
    assert d.parent == base
