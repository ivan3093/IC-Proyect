from pathlib import Path
from src.report.charts import build_bar_chart_png


def test_build_bar_chart_png(tmp_path):
    counts = {"ERROR": 3, "WARNING": 2, "INFO": 1}
    out = build_bar_chart_png(counts, out_dir=tmp_path, filename="plot.png")
    assert out.exists() and out.suffix == ".png"
