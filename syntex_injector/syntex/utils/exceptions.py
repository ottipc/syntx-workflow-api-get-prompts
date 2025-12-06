"""
SYNTEX Custom Exceptions
"""


class SyntexException(Exception):
    """Base Exception für alle SYNTEX Fehler"""
    pass


class WrapperNotFoundError(SyntexException):
    """SYNTEX Wrapper-Datei nicht gefunden"""
    pass


class InvalidResponseError(SyntexException):
    """Model Response entspricht nicht SYNTEX Format"""
    pass


class FieldMissingError(SyntexException):
    """Ein oder mehrere SYNTEX Felder fehlen"""
    def __init__(self, missing_fields):
        self.missing_fields = missing_fields
        super().__init__(f"Missing SYNTEX fields: {', '.join(missing_fields)}")


class CalibrationFailedError(SyntexException):
    """Kalibrierung fehlgeschlagen"""
    pass


class ParseError(SyntexException):
    """Fehler beim Parsen der SYNTEX Response"""
    pass
