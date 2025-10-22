Log Analyzer API

    Small FastAPI service that analyzes plaintext server logs ( .txt ), classifies lines by severity (ERROR, WARNING, INFO), returns a JSON summary, and generates a shareable HTML report.

Features

    POST /analyze-file accepts a local .txt upload (multipart/form-data).

    Strict UTF-8 decode (fail fast, helpful error messages).

    Line-by-line streaming parse with regex (tolerant to spaces, case-insensitive levels).

    Output JSON: {'ERROR':[], 'WARNING':[], 'INFO':[]} + counts + percentages + tops.

    HTML report (Jinja2) with totals, percentages, “top error” and “top warning”, plus samples (first/last N).

    Static files served at /reports/<uuid>/... (report.html + assets).

Out-of-scope (for now): remote URLs/S3, auth, non-UTF-8 encodings, formats other than .txt.

PROYECT LAYOUT
app/
  main.py                # FastAPI endpoint + static mount + error mapping
src/
  core/
    parser.py            # regex-based parse_line + log_analyzer(streaming)
    metrics.py           # counts, percents, top repeated (+ samples helper)
  service/
    analyze.py           # orchestrates: decode -> core -> metrics -> artifacts
  report/
    charts.py            # bar chart PNG (severity)  [MVP or next]
    builder.py           # Jinja2 HTML report
  io/
    validators.py        # .txt extension, MIME checks
  utils/
    errors.py            # DecodeError, FormatError, UnknownLevel, etc.
    files.py             # artifacts dir /static/reports/<uuid>/
  schemas/
    responses.py         # Pydantic models for API responses
templates/
  report.html.j2         # HTML template
static/
  reports/               # generated artifacts (mounted at /reports)
tests/
  ...                    # pytest suite (unit + integration)

TESTS
    Unit test can be performed with:
    pytest -q

source venv/bin/activate && python -m uvicorn app.main:app --reload
