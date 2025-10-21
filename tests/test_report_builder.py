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

def test_build_report_html_with_samples(tmp_path, tmp_template_dir):
    result = {"ERROR":["[ERROR] A","[ERROR] B"], "WARNING":["[WARNING] C"], "INFO":["[INFO] D"]}
    metrics = {
        "counts":{"ERROR":2,"WARNING":1,"INFO":1,"INVALID":0},
        "percent":{"ERROR":50.0,"WARNING":25.0,"INFO":25.0},
        "top":{"ERROR":{"message":"[ERROR] A","count":1},"WARNING":None},
        "duration_ms":10,
    }
    (tmp_path / "severity.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    samples = {
        "ERROR":{"first":["[ERROR] A"],"last":["[ERROR] B"]},
        "WARNING":{"first":["[WARNING] C"],"last":["[WARNING] C"]},
        "INFO":{"first":["[INFO] D"],"last":["[INFO] D"]},
    }
    out = build_report_html(
        result=result,
        metrics=metrics,
        samples=samples,
        out_dir=tmp_path,
        template_path=tmp_template_dir / "report.html.j2",
    )
    html = out.read_text(encoding="utf-8")
    assert "Primeras" in html and "Últimas" in html
    assert "[ERROR] A" in html and "[ERROR] B" in html

