"""
SYNTEX Response Parser
Extrahiert strukturierte Felder aus Model-Responses
"""

import re
from typing import Dict, Optional, List
from dataclasses import dataclass

from ..utils.exceptions import ParseError, FieldMissingError


@dataclass
class SyntexFields:
    """Strukturierte SYNTEX Felder"""
    driftkoerper: Optional[str] = None
    subprotokoll: Optional[str] = None
    kalibrierungsfeld: Optional[str] = None
    tier: Optional[str] = None
    resonanzsplit: Optional[str] = None
    klartext: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "driftkoerper": self.driftkoerper,
            "subprotokoll": self.subprotokoll,
            "kalibrierungsfeld": self.kalibrierungsfeld,
            "tier": self.tier,
            "resonanzsplit": self.resonanzsplit,
            "klartext": self.klartext
        }
    
    def missing_fields(self) -> List[str]:
        """Gibt Liste der fehlenden Felder zurück"""
        missing = []
        for field, value in self.to_dict().items():
            if value is None or value.strip() == "":
                missing.append(field)
        return missing
    
    def is_complete(self) -> bool:
        """Prüft ob alle Felder vorhanden sind"""
        return len(self.missing_fields()) == 0


class SyntexParser:
    """Parst SYNTEX-Responses und extrahiert Felder"""
    
    PATTERNS = {
        "driftkoerper": r"1\.\s*DRIFTK[ÖO]RPER[:\s]*(.*?)(?=\n\s*2\.|$)",
        "subprotokoll": r"2\.\s*SUBPROTOKO?LL?[:\s]*(.*?)(?=\n\s*3\.|$)",
        "kalibrierungsfeld": r"3\.\s*KALIBRIERUNGSFELD[:\s]*(.*?)(?=\n\s*4\.|$)",
        "tier": r"4\.\s*TIER[-\s]*ANAL[YS][SE][:\s]*(.*?)(?=\n\s*5\.|$)",
        "resonanzsplit": r"5\.\s*RESONANZSPLIT[:\s]*(.*?)(?=\n\s*6\.|$)",
        "klartext": r"6\.\s*KLARTEXT[:\s]*(.*?)$"
    }
    
    def __init__(self):
        self.compiled_patterns = {
            field: re.compile(pattern, re.IGNORECASE | re.DOTALL)
            for field, pattern in self.PATTERNS.items()
        }
    
    def parse(self, response: str) -> SyntexFields:
        """Parst SYNTEX Response und extrahiert Felder."""
        if not response or response.strip() == "":
            raise ParseError("Empty response")
        
        fields = SyntexFields()
        
        for field_name, pattern in self.compiled_patterns.items():
            match = pattern.search(response)
            if match:
                content = match.group(1).strip()
                setattr(fields, field_name, content)
        
        return fields
    
    def validate(self, fields: SyntexFields, strict: bool = False) -> bool:
        """Validiert ob alle SYNTEX Felder vorhanden sind."""
        missing = fields.missing_fields()
        
        if missing and strict:
            raise FieldMissingError(missing)
        
        return len(missing) == 0
