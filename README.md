Log Analyzer API

    Small FastAPI service that analyzes plaintext server logs ( .txt ), classifies lines by severity (ERROR, WARNING, INFO), returns a JSON summary, and generates a shareable HTML report.

QuickStart
    Requirements
        Python 3.10+
        virtualenv

    Setup
        python3 -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt

    Run
        uvicorn app.main:app --reload
        # Open Swagger: 
        http://127.0.0.1:8000/docs

    Try
        Open Swagger or cURL POSTMAN

            CURL
            curl -s -X POST "http://127.0.0.1:8000/analyze-file" \
            -F "file=@./server_logs.txt;type=text/plain" | jq
    File Format
        Analyze-file Endpoint currently support .txt files in the following format:
            [INFO] Server started successfully
            [WARNING] Low available memory
            [ERROR] Database connection failed
        There is a couple sample FIles for testing included:
            testtxt.txt #with an small test sample
            mock_logs_100 #With a 100 logs sample
    Result Output:
        JSON with:
            The logs classified by ERROR
            The logs CLassified By WARNING
            The logs Classified by INFO
            Log FIle Metrics:
                Count for each Log type (ERROR,WARNING,INFO)
                Distribution percent by type
                top N (default 3) most repeated
                    Errors
                    Warnings
            URL to a complementary proyect report in HTML
                Report Contains:
                    Most repeated Errors and Warnings
                    First N (default 3) Error Lines (from resulting Dictionary)
                    Last N (default 3) Error Lines (from resulting Dictionary)
                    First N (default 3) Warning Lines (from resulting Dictionary)
                    Last N (default 3) Warning Lines (from resulting Dictionary)
                    First N (default 3) INFO Lines (from resulting Dictionary)
                    Last N (default 3) INFO Lines (from resulting Dictionary)

            URL to a complementary Bar Graph PNG 
                Bar Graph showcases:
                    Number of logs by severity


Features

    POST /analyze-file accepts a local .txt upload (multipart/form-data).

    Strict UTF-8 decode (fail fast, helpful error messages).

    Line-by-line streaming parse with regex (tolerant to spaces, case-insensitive levels).

    Output JSON: {'ERROR':[], 'WARNING':[], 'INFO':[]} + counts + percentages + tops.

    HTML report (Jinja2) with totals, percentages, “top error” and “top warning”, plus samples (first/last N).

    Static files served at /reports/<uuid>/... (report.html + assets).

    Other Endpoints for tests and mock login including
        GET /gitstats
            #checks that the proyect is connected to GIt
        GET /health
            #Chech that all dependencies are installed
        POST /api/v1/auth/token
            #Generates a mock authentication Token (not needed)
        POST /api/v1/auth/token-expired
            #Generates an expired mock authentication Token (not needed)
        POST /api/v1/validateUser
            #Mock User Validation to simulate a login (not needed)
                mock_users = [
                {"userId": "usr_12345", "email": "user@example.com", "status": "active"},
                {"userId": "usr_67890", "email": "admin@example.com", "status": "suspended"}
                ]
        POST /analyze-file
            #Main Proyect Feature Receives a .txt file via multipart/form-data (see requirements)


Out-of-scope (for now): remote URLs/S3, auth, non-UTF-8 encodings, formats other than .txt.

PROYECT LAYOUT

''''

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
    
''''    

TESTS
    Unit test can be performed with:
    pytest -q

    Tests Cover: 
        Core parser
            Happy path
            Format Error
            Unknown Log Level
            Fail Fast Format
                On Invalid Line Format
                On Unknown Level

        Metrics 
            Top Repeated
            Build Metrics Distribution
            Top Error
            Top Warning

        Builder/Charts 
            Report Build top List
            Report Build HTML
            Build Bar Chart

        Service orchestrator
            File Format not text/plain/octet-stream
            File content not text/plain/octet-stream

        Endpoint
            Happy path
            Format Error
            Unknown Log Level
            Decode Error

CONFIGURATION

    UTF-8 only

    .txt extention required

    text/plain and applicatio/octet-stream accepted with .txt

    HTML and PNG reports saved under static/reports/<'uuid>'/ 
        exposed at /reports/<'reportId>'/report.html 
        and 
        /reports/<'reportId>'/severity.png

Troubleshooting

    404 when opening report_url_html
        Use the full absolute URL. Ensure app.mount("/reports", ...) is present and static/reports/<uuid>/report.html exists on disk.

    415 DecodeError
        The uploaded file isn’t UTF-8. Re-save as UTF-8 and try again.

    422 UnknownLevel / FormatError
        Line format must be [LEVEL] message, levels in {INFO, WARNING, ERROR} (case-insensitive).

    Startup error “Missing report template”
        Ensure templates/report.html.j2 exists and app.main resolves the correct project root for the template path.

    Deprecation warnings (on_event)
        Non-blocking. Can be migrated to FastAPI Lifespan later.

Security / Limits
    No authentication; intended for local/demo use.

    File size: keep modest (e.g., <10MB). We read line-by-line, but PNG/HTML generation still writes to disk.

    No remote fetch; uploads only.


Credits

Built by Iván Garcia Aguirre.

Stack: FastAPI, Uvicorn, Starlette, Pydantic, Jinja2, Matplotlib, python-multipart, PyTest.
