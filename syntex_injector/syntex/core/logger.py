"""
SYNTEX Calibration Logging System
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any


class CalibrationLogger:
    """Loggt SYNTEX Kalibrierungs-Prozesse"""
    
    def __init__(self, log_file: Optional[Path] = None):
        self.log_file = log_file or Path("logs/syntex_calibrations.jsonl")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log_calibration(
        self,
        meta_prompt: str,
        full_prompt: str,
        response: Optional[str],
        success: bool,
        duration_ms: int,
        retry_count: int,
        error: Optional[str] = None,
        model_params: Optional[Dict] = None,
        quality_score: Optional[Dict] = None,
        parsed_fields: Optional[Dict] = None
    ) -> None:
        """Loggt eine SYNTEX-Kalibrierung mit allen Metriken"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "system": "SYNTEX::TRUE_RAW",
            "meta_prompt": meta_prompt,
            "meta_prompt_length": len(meta_prompt),
            "full_prompt_length": len(full_prompt),
            "response": response,
            "response_length": len(response) if response else 0,
            "success": success,
            "error": error,
            "duration_ms": duration_ms,
            "retry_count": retry_count,
            "model_params": model_params or {},
            "quality_score": quality_score,
            "parsed_fields": parsed_fields
        }
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def get_last_calibrations(self, n: int = 10) -> list:
        """Gibt die letzten N Kalibrierungen zurück"""
        if not self.log_file.exists():
            return []
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        return [json.loads(line) for line in lines[-n:]]
