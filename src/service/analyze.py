from typing import Tuple, Dict, List
from pathlib import Path
import time
from fastapi import UploadFile
from src.core.parser import log_analyzer
from src.core.metrics import build_metrics, build_samples
from src.report.charts import build_bar_chart_png
from src.report.builder import build_report_html
from src.utils.files import make_artifacts_dir
from src.utils.errors import DecodeError, IOErrorApp


PROJECT_ROOT = Path(__file__).resolve().parents[2]  # .../log-analyzer/
TEMPLATE_FILE = PROJECT_ROOT / "templates" / "report.html.j2"


def analyze_from_upload(file: UploadFile) -> Tuple[Dict[str, List[str]], dict, Path]:
    """
    Reads an UploadFile (forcing UTF-8), classifies line by line, computes metrics,
    and generates artifacts (PNG + HTML). Returns:
        (result_dict, metrics_dict, report_html_path, png_path)
    Raises:
        DecodeError, IOErrorApp, FormatError, UnknownLevel, ValidationError
    """
    started = time.time()

    try:
        # Forces decodification UTF-8 on streaming
        # Nota: UploadFile.file is a SpooledTemporaryFile; we read line by line
        lines: List[str] = []
        for raw in file.file:
            try:
                lines.append(raw.decode("utf-8"))
            except UnicodeDecodeError as e:
                # maps explicit to decodeError
                raise DecodeError(f"UTF-8 decoding failed at byte offset. {e}") from e
    
    except DecodeError:
        raise
    except Exception as e:
        # other reading errors => 400
        raise IOErrorApp(f"Error reading uploaded file: {e}") from e

    # Core parsing (can throw FormatError/UnknownLevel)
    result = log_analyzer(lines)

    # Metrics
    duration_ms = int((time.time() - started) * 1000)
    metrics = build_metrics(result, invalid_count=0, duration_ms=duration_ms)

    # samples for the report (first/last N)
    samples = build_samples(result, n=3)

    # Artifacts: creates directory /static/reports/{uuid}/
    out_dir = make_artifacts_dir(base=Path("static") / "reports")
    png_path = build_bar_chart_png(metrics["counts"], out_dir)

    report_path = build_report_html(
        result=result,
        metrics=metrics,
        samples=samples,  # <-- new parameter
        out_dir=out_dir,
        #template_path=Path("templates") / "report.html.j2",
        template_path=TEMPLATE_FILE,  # <-- absolute path
    )
    return result, metrics, report_path ,png_path
