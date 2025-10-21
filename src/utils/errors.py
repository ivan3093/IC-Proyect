class AppBaseError(Exception):
    """Base para errores controlados de la app."""
    pass


class ValidationError(AppBaseError):
    pass


class DecodeError(AppBaseError):
    pass


class IOErrorApp(AppBaseError):
    pass


class _LineContextError(AppBaseError):
    """Errores con contexto de línea (fallo y última OK)."""
    def __init__(self, line_no: int, line: str, last_ok_no=None, last_ok_line=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed_line_number = line_no
        self.failed_line_content = line
        self.last_success_line_number = last_ok_no
        self.last_success_line_content = last_ok_line


class FormatError(_LineContextError):
    def __str__(self):
        return f"Invalid format at line {self.failed_line_number}."


class UnknownLevel(_LineContextError):
    def __str__(self):
        return f"Unknown level at line {self.failed_line_number}."
