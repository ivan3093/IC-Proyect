from src.report.builder import build_report_html

def test_build_report_html_top_list(tmp_path, tmp_template_dir):
    result = {
        "ERROR": ["[ERROR] e1", "[ERROR] e2", "[ERROR] e1"],
        "WARNING": ["[WARNING] w1"],
        "INFO": ["[INFO] i1"],
    }
    metrics = {
        "counts": {"ERROR": 3, "WARNING": 1, "INFO": 1, "INVALID": 0},
        "percent": {"ERROR": 60.0, "WARNING": 20.0, "INFO": 20.0},
        "top": {
            "ERROR": [{"message": "[ERROR] e1", "count": 2}, {"message": "[ERROR] e2", "count": 1}],
            "WARNING": [{"message": "[WARNING] w1", "count": 1}],
        },
        "duration_ms": 10,
    }
    (tmp_path / "severity.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    out = build_report_html(
        result=result,
        metrics=metrics,
        out_dir=tmp_path,
        template_path=tmp_template_dir / "report.html.j2",
    )
    html = out.read_text(encoding="utf-8")
    assert out.exists()
    assert "ERROR: 3" in html  # si tu template muestra conteos
    assert "[ERROR] e1" in html and "2" in html
