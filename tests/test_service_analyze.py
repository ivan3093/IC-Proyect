import io
import pytest
from starlette.datastructures import UploadFile
from src.service.analyze import analyze_from_upload
from src.utils.errors import DecodeError, FormatError, UnknownLevel


def test_analyze_from_upload_happy(upload_txt_ok):
    result, metrics, report_path, png_path = analyze_from_upload(upload_txt_ok)
    assert set(result.keys()) == {"ERROR", "WARNING", "INFO"}
    assert "counts" in metrics and "percent" in metrics
    assert report_path.exists()
    assert png_path.exists()


def test_analyze_from_upload_format_error(upload_txt_invalid):
    with pytest.raises(FormatError):
        analyze_from_upload(upload_txt_invalid)


def test_analyze_from_upload_unknown(upload_txt_unknown):
    with pytest.raises(UnknownLevel):
        analyze_from_upload(upload_txt_unknown)


def test_analyze_from_upload_decode_error(upload_txt_non_utf8):
    with pytest.raises(DecodeError):
        analyze_from_upload(upload_txt_non_utf8)
