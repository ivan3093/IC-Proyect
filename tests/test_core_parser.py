import pytest
from src.core.parser import parse_line, log_analyzer
from src.utils.errors import FormatError, UnknownLevel


def test_parse_line_happy():
    lvl, msg = parse_line("   [warning]  memory low   ", 7)
    assert lvl == "WARNING"
    assert msg == "memory low"


def test_parse_line_format_error():
    with pytest.raises(FormatError) as e:
        parse_line("no-brackets here", 2)
    assert "Invalid format" in str(e.value)


def test_parse_line_unknown_level():
    with pytest.raises(UnknownLevel) as e:
        parse_line("[ALERT] something", 3)
    assert "Unknown level" in str(e.value)


def test_log_analyzer_happy(sample_ok_lines):
    res = log_analyzer(sample_ok_lines)
    assert set(res.keys()) == {"ERROR", "WARNING", "INFO"}
    assert len(res["ERROR"]) >= 1
    assert any(s.startswith("[WARNING]") for s in res["WARNING"])
    assert any(s.startswith("[INFO]") for s in res["INFO"])


def test_log_analyzer_fail_fast_format(sample_invalid_line):
    with pytest.raises(FormatError) as e:
        log_analyzer(sample_invalid_line)
    err = e.value
    assert err.failed_line_number == 2
    # La última línea OK fue la 1
    assert getattr(err, "last_success_line_number", None) == 1


def test_log_analyzer_fail_fast_unknown(sample_unknown_level):
    with pytest.raises(UnknownLevel) as e:
        log_analyzer(sample_unknown_level)
    err = e.value
    assert err.failed_line_number == 2
    assert getattr(err, "last_success_line_number", None) == 1
