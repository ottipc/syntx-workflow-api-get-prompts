"""
SYNTEX Response Parser
Extrahiert strukturierte Felder aus Model-Responses
Unterstützt beide Terminologien: Technisch (DRIFTKÖRPER) und Menschlich (DRIFT)
"""

import re
from typing import Dict, Optional, List
from dataclasses import dataclass

from ..utils.exceptions import ParseError, FieldMissingError


@dataclass
class SyntexFields:
    """Strukturierte SYNTEX Felder"""
    drift: Optional[str] = None
    hintergrund_muster: Optional[str] = None
    druckfaktoren: Optional[str] = None
    tiefe: Optional[str] = None
    wirkung: Optional[str] = None
    klartext: Optional[str] = None
    
    # Aliases für alte Terminologie
    @property
    def driftkoerper(self):
        return self.drift
    
    @property
    def subprotokoll(self):
        return self.hintergrund_muster
    
    @property
    def kalibrierungsfeld(self):
        return self.druckfaktoren
    
    @property
    def tier(self):
        return self.tiefe
    
    @property
    def resonanzsplit(self):
        return self.wirkung
    
    def to_dict(self) -> Dict:
        return {
            "drift": self.drift,
            "hintergrund_muster": self.hintergrund_muster,
            "druckfaktoren": self.druckfaktoren,
            "tiefe": self.tiefe,
            "wirkung": self.wirkung,
            "klartext": self.klartext,
            # Alte Namen für Kompatibilität
            "driftkoerper": self.drift,
            "subprotokoll": self.hintergrund_muster,
            "kalibrierungsfeld": self.druckfaktoren,
            "tier": self.tiefe,
            "resonanzsplit": self.wirkung
        }
    
    def missing_fields(self) -> List[str]:
        """Gibt Liste der fehlenden Felder zurück"""
        missing = []
        core_fields = {
            "drift": self.drift,
            "hintergrund_muster": self.hintergrund_muster,
            "druckfaktoren": self.druckfaktoren,
            "tiefe": self.tiefe,
            "wirkung": self.wirkung,
            "klartext": self.klartext
        }
        for field, value in core_fields.items():
            if value is None or value.strip() == "":
                missing.append(field)
        return missing
    
    def is_complete(self) -> bool:
        """Prüft ob alle Felder vorhanden sind"""
        return len(self.missing_fields()) == 0


class SyntexParser:
    """Parst SYNTEX-Responses und extrahiert Felder (beide Terminologien)"""
    
    # Patterns für BEIDE Terminologien
    PATTERNS = {
        # Neue menschliche Terminologie
        "drift": r"1\.\s*DRIFT[:\s]*(.*?)(?=\n\s*2\.|$)",
        "hintergrund_muster": r"2\.\s*HINTERGRUND[-\s]*MUSTER[:\s]*(.*?)(?=\n\s*3\.|$)",
        "druckfaktoren": r"3\.\s*DRUCKFAKTOREN[:\s]*(.*?)(?=\n\s*4\.|$)",
        "tiefe": r"4\.\s*TIEFE[:\s]*(.*?)(?=\n\s*5\.|$)",
        "wirkung": r"5\.\s*WIRKUNG\s+AUF\s+BEIDE\s+SEITEN[:\s]*(.*?)(?=\n\s*6\.|$)",
        "klartext": r"6\.\s*KLARTEXT[:\s]*(.*?)$",
        
        # Alte technische Terminologie (Fallback)
        "drift_alt": r"1\.\s*DRIFTK[ÖO]RPER[:\s]*(.*?)(?=\n\s*2\.|$)",
        "hintergrund_alt": r"2\.\s*SUBPROTOKO?LL?[:\s]*(.*?)(?=\n\s*3\.|$)",
        "druck_alt": r"3\.\s*KALIBRIERUNGSFELD[:\s]*(.*?)(?=\n\s*4\.|$)",
        "tiefe_alt": r"4\.\s*TIER[-\s]*ANAL[YS][SE][:\s]*(.*?)(?=\n\s*5\.|$)",
        "wirkung_alt": r"5\.\s*RESONANZSPLIT[:\s]*(.*?)(?=\n\s*6\.|$)"
    }
    
    def __init__(self):
        self.compiled_patterns = {
            field: re.compile(pattern, re.IGNORECASE | re.DOTALL)
            for field, pattern in self.PATTERNS.items()
        }
    
    def parse(self, response: str) -> SyntexFields:
        """
        Parst SYNTEX Response und extrahiert Felder.
        Unterstützt beide Terminologien automatisch.
        """
        if not response or response.strip() == "":
            raise ParseError("Empty response")
        
        fields = SyntexFields()
        
        # Neue Terminologie (Priorität)
        for field_name in ["drift", "hintergrund_muster", "druckfaktoren", "tiefe", "wirkung", "klartext"]:
            pattern = self.compiled_patterns.get(field_name)
            if pattern:
                match = pattern.search(response)
                if match:
                    content = match.group(1).strip()
                    setattr(fields, field_name, content)
        
        # Fallback auf alte Terminologie
        if not fields.drift and "drift_alt" in self.compiled_patterns:
            match = self.compiled_patterns["drift_alt"].search(response)
            if match:
                fields.drift = match.group(1).strip()
        
        if not fields.hintergrund_muster and "hintergrund_alt" in self.compiled_patterns:
            match = self.compiled_patterns["hintergrund_alt"].search(response)
            if match:
                fields.hintergrund_muster = match.group(1).strip()
        
        if not fields.druckfaktoren and "druck_alt" in self.compiled_patterns:
            match = self.compiled_patterns["druck_alt"].search(response)
            if match:
                fields.druckfaktoren = match.group(1).strip()
        
        if not fields.tiefe and "tiefe_alt" in self.compiled_patterns:
            match = self.compiled_patterns["tiefe_alt"].search(response)
            if match:
                fields.tiefe = match.group(1).strip()
        
        if not fields.wirkung and "wirkung_alt" in self.compiled_patterns:
            match = self.compiled_patterns["wirkung_alt"].search(response)
            if match:
                fields.wirkung = match.group(1).strip()
        
        return fields
    
    def validate(self, fields: SyntexFields, strict: bool = False) -> bool:
        """Validiert ob alle SYNTEX Felder vorhanden sind."""
        missing = fields.missing_fields()
        
        if missing and strict:
            raise FieldMissingError(missing)
        
        return len(missing) == 0
