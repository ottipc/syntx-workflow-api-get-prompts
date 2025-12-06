"""
SYNTEX Response Parser - Simple SIGMA Detection
"""

import re
from typing import Dict, Optional, List
from dataclasses import dataclass

from ..utils.exceptions import ParseError, FieldMissingError


@dataclass
class SyntexFields:
    """SYNTEX Felder - alle Terminologien"""
    drift: Optional[str] = None
    hintergrund_muster: Optional[str] = None
    druckfaktoren: Optional[str] = None
    tiefe: Optional[str] = None
    wirkung: Optional[str] = None
    klartext: Optional[str] = None
    
    sigma_drift: Optional[str] = None
    sigma_mechanismus: Optional[str] = None
    sigma_frequenz: Optional[str] = None
    sigma_dichte: Optional[str] = None
    sigma_strome: Optional[str] = None
    sigma_extrakt: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "drift": self.drift,
            "hintergrund_muster": self.hintergrund_muster,
            "druckfaktoren": self.druckfaktoren,
            "tiefe": self.tiefe,
            "wirkung": self.wirkung,
            "klartext": self.klartext,
            "sigma_drift": self.sigma_drift,
            "sigma_mechanismus": self.sigma_mechanismus,
            "sigma_frequenz": self.sigma_frequenz,
            "sigma_dichte": self.sigma_dichte,
            "sigma_strome": self.sigma_strome,
            "sigma_extrakt": self.sigma_extrakt
        }
    
    def missing_fields(self) -> List[str]:
        missing = []
        
        if self.is_sigma():
            sigma_fields = {
                "sigma_drift": self.sigma_drift,
                "sigma_mechanismus": self.sigma_mechanismus,
                "sigma_frequenz": self.sigma_frequenz,
                "sigma_dichte": self.sigma_dichte,
                "sigma_strome": self.sigma_strome,
                "sigma_extrakt": self.sigma_extrakt
            }
            for field, value in sigma_fields.items():
                if value is None or value.strip() == "":
                    missing.append(field)
        else:
            human_fields = {
                "drift": self.drift,
                "hintergrund_muster": self.hintergrund_muster,
                "druckfaktoren": self.druckfaktoren,
                "tiefe": self.tiefe,
                "wirkung": self.wirkung,
                "klartext": self.klartext
            }
            for field, value in human_fields.items():
                if value is None or value.strip() == "":
                    missing.append(field)
        
        return missing
    
    def is_complete(self) -> bool:
        return len(self.missing_fields()) == 0
    
    def is_sigma(self) -> bool:
        return any([
            self.sigma_drift,
            self.sigma_mechanismus,
            self.sigma_frequenz,
            self.sigma_dichte,
            self.sigma_strome,
            self.sigma_extrakt
        ])


class SyntexParser:
    """Simple Parser für alle Terminologien"""
    
    def __init__(self):
        pass
    
    def parse(self, response: str) -> SyntexFields:
        if not response or response.strip() == "":
            raise ParseError("Empty response")
        
        fields = SyntexFields()
        
        # Detect SIGMA
        if "Σ-DRIFTGRADIENT" in response or "Σ-MECHANISMUSKNOTEN" in response:
            # Simple SIGMA extraction - alles nach "1." bis "2."
            patterns = [
                (r"1\.\s*Σ-DRIFTGRADIENT.*?(?=2\.|$)", "sigma_drift"),
                (r"2\.\s*Σ-MECHANISMUSKNOTEN.*?(?=3\.|$)", "sigma_mechanismus"),
                (r"3\.\s*Σ-FREQUENZFELD.*?(?=4\.|$)", "sigma_frequenz"),
                (r"4\.\s*Σ-DICHTELEVEL.*?(?=5\.|$)", "sigma_dichte"),
                (r"5\.\s*Σ-ZWEISTRÖME.*?(?=6\.|$)", "sigma_strome"),
                (r"6\.\s*Σ-KERNEXTRAKT.*?$", "sigma_extrakt")
            ]
            
            for pattern, field_name in patterns:
                match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
                if match:
                    content = match.group(0).strip()
                    # Remove field header
                    content = re.sub(r"^\d+\.\s*Σ-[A-Z]+\s*[-:]?\s*", "", content, flags=re.IGNORECASE)
                    setattr(fields, field_name, content.strip())
        
        else:
            # Menschliche Terminologie
            patterns = [
                (r"1\.\s*DRIFT[:\s]*(.*?)(?=\n\s*2\.|$)", "drift"),
                (r"2\.\s*HINTERGRUND[-\s]*MUSTER[:\s]*(.*?)(?=\n\s*3\.|$)", "hintergrund_muster"),
                (r"3\.\s*DRUCKFAKTOREN[:\s]*(.*?)(?=\n\s*4\.|$)", "druckfaktoren"),
                (r"4\.\s*TIEFE[:\s]*(.*?)(?=\n\s*5\.|$)", "tiefe"),
                (r"5\.\s*WIRKUNG.*?(?=\n\s*6\.|$)", "wirkung"),
                (r"6\.\s*KLARTEXT[:\s]*(.*?)$", "klartext")
            ]
            
            for pattern, field_name in patterns:
                match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
                if match:
                    if match.lastindex:
                        setattr(fields, field_name, match.group(1).strip())
                    else:
                        content = match.group(0).strip()
                        content = re.sub(r"^\d+\.\s*[A-Z\s]+[:\s]*", "", content, flags=re.IGNORECASE)
                        setattr(fields, field_name, content.strip())
        
        return fields
    
    def validate(self, fields: SyntexFields, strict: bool = False) -> bool:
        missing = fields.missing_fields()
        if missing and strict:
            raise FieldMissingError(missing)
        return len(missing) == 0
