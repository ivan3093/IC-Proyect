from typing import Dict, List, Tuple, Optional, Any
from collections import Counter

def top_repeated(messages: List[str], n: int = 3) -> List[Tuple[str, int]]:
    """
    Retorna una lista con los `n` mensajes más repetidos y sus conteos.
    Retorna lista vacía si no hay mensajes.
    """
    if not messages:
        return []
    c = Counter(messages)
    return c.most_common(n)

def build_metrics(result: Dict[str, List[str]], invalid_count: int = 0, duration_ms: int = 0) -> Dict:
    """
    Calcula conteos, % relativos y tops (ERROR/WARNING).
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

    # Obtener top 3 para ERROR y WARNING
    top_err = top_repeated(result.get("ERROR", []))
    top_warn = top_repeated(result.get("WARNING", []))

    # Convertir a lista de diccionarios o None si está vacío
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
