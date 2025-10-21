import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_endpoint_happy():
    content = b"[INFO] ok\n[WARNING] w\n[ERROR] e\n"
    files = {"file": ("server_logs.txt", io.BytesIO(content), "text/plain")}
    r = client.post("/analyze-file", files=files)
    assert r.status_code == 200
    j = r.json()
    assert "result" in j and "metrics" in j and "report_url_html" in j
    assert j["result"]["ERROR"] and j["result"]["INFO"]


def test_endpoint_format_error():
    content = b"[INFO] ok\nbroken_line\n"
    files = {"file": ("server_logs.txt", io.BytesIO(content), "text/plain")}
    r = client.post("/analyze-file", files=files)
    assert r.status_code == 422
    j = r.json()
    assert "FormatError" in j["detail"]["error_type"]
    assert j["detail"]["failed_line_number"] == 2


def test_endpoint_unknown_level():
    content = b"[INFO] ok\n[ALERT] z\n"
    files = {"file": ("server_logs.txt", io.BytesIO(content), "text/plain")}
    r = client.post("/analyze-file", files=files)
    assert r.status_code == 422
    j = r.json()
    assert "UnknownLevel" in j["detail"]["error_type"]
    assert j["detail"]["failed_line_number"] == 2


def test_endpoint_decode_error():
    content = b"\xff\xfe\xfa"
    files = {"file": ("server_logs.txt", io.BytesIO(content), "text/plain")}
    r = client.post("/analyze-file", files=files)
    assert r.status_code == 415
    j = r.json()
    assert "DecodeError" in j["detail"]["error_type"]
