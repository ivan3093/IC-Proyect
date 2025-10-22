from typing import Dict, List, Tuple, Optional, Any
from collections import Counter

def top_repeated(messages: List[str], n: int = 3) -> List[Tuple[str, int]]:
    """
    Returns a list with the top `n` most repeated messages and their counts.
    Returns an empty list if there are no messages.
    """
    if not messages:
        return []
    c = Counter(messages)
    return c.most_common(n)

def build_metrics(result: Dict[str, List[str]], invalid_count: int = 0, duration_ms: int = 0) -> Dict:
    """
    Computes counts, relative percentages, and tops (ERROR/WARNING).
    Returns:
        {
          'counts': {'ERROR': int, 'WARNING': int, 'INFO': int, 'INVALID': int},
          'percent': {'ERROR': float, 'WARNING': float, 'INFO': float},
          'top': {
              'ERROR': [{'message': str, 'count': int}] | None,  # Top 3
              'WARNING': [{'message': str, 'count': int}] | None # Top 3
          },
          'duration_ms': int
        }
    """
    counts = {k: len(v) for k, v in result.items()}
    total_valid = sum(counts.values())
    percent = {
        k: (counts[k] / total_valid * 100.0) if total_valid else 0.0
        for k in ("ERROR", "WARNING", "INFO")
    }
    counts["INVALID"] = invalid_count

    # Get top 3 for ERROR and WARNING
    top_err = top_repeated(result.get("ERROR", []))
    top_warn = top_repeated(result.get("WARNING", []))

    # Convert to list of dicts or None if empty
    top = {
        "ERROR": [{"message": msg, "count": count} for msg, count in top_err] if top_err else None,
        "WARNING": [{"message": msg, "count": count} for msg, count in top_warn] if top_warn else None,
    }

    return {
        "counts": counts,
        "percent": percent,
        "top": top,
        "duration_ms": duration_ms,
    }

def build_samples(result: Dict[str, List[str]], n: int = 3) -> Dict[str, Dict[str, List[str]]]:
    """
    Returns, per severity, the first and last N lines.
    Estructura:
    {
      "ERROR":   {"first": [...], "last": [...]},
      "WARNING": {"first": [...], "last": [...]},
      "INFO":    {"first": [...], "last": [...]}
    }
    """
    out: Dict[str, Dict[str, List[str]]] = {}
    for level in ("ERROR", "WARNING", "INFO"):
        lines = result.get(level, [])
        out[level] = {
            "first": lines[:n],
            "last":  lines[-n:] if len(lines) >= n else lines[:],
        }
    return out
