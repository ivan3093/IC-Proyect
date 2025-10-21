from src.core.metrics import build_metrics, top_repeated

def test_top_repeated_basic():
    tops = top_repeated(["a","b","a","a","c"])  # top N, default 3
    # Esperamos lista de tuplas [(msg, count), ...]
    assert isinstance(tops, list)
    assert len(tops) >= 1
    assert tops[0] == ("a", 3)  # primer lugar correcto
    # y ordenado desc por conteo
    counts = [c for _, c in tops]
    assert counts == sorted(counts, reverse=True)

def test_build_metrics_distribution():
    result = {
        "ERROR": ["[ERROR] e1", "[ERROR] e2", "[ERROR] e1"],
        "WARNING": ["[WARNING] w1"],
        "INFO": ["[INFO] i1", "[INFO] i2"],
    }
    m = build_metrics(result, invalid_count=0, duration_ms=123)

    assert m["counts"]["ERROR"] == 3
    assert m["counts"]["WARNING"] == 1
    assert m["counts"]["INFO"] == 2
    assert m["percent"]["ERROR"] > m["percent"]["WARNING"]

    # Ahora top es lista de dicts
    top_err = m["top"]["ERROR"]
    assert isinstance(top_err, list)
    assert top_err[0]["message"] == "[ERROR] e1"
    assert top_err[0]["count"] == 2

    top_warn = m["top"]["WARNING"]
    assert isinstance(top_warn, list)
    assert top_warn[0]["message"] == "[WARNING] w1"
    assert top_warn[0]["count"] == 1

    assert m["duration_ms"] == 123
