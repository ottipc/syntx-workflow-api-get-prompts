"""
SYNTEX Calibration Engine
Kern-Logik für Resonanz-Kalibrierung
"""

import time
from pathlib import Path
from typing import Optional, Tuple, Dict

from .wrapper import SyntexWrapper
from .logger import CalibrationLogger
from ..api.client import APIClient
from ..api.config import MODEL_PARAMS


class SyntexCalibrator:
    """
    SYNTEX::TRUE_RAW Kalibrierungs-Engine
    
    Kombiniert Wrapper, API Client und Logger
    für semantische Strom-Analyse
    """
    
    def __init__(
        self,
        wrapper_file: Optional[Path] = None,
        log_file: Optional[Path] = None
    ):
        self.wrapper = SyntexWrapper(wrapper_file)
        self.client = APIClient()
        self.logger = CalibrationLogger(log_file)
    
    def calibrate(
        self,
        meta_prompt: str,
        verbose: bool = True
    ) -> Tuple[bool, Optional[str], Dict]:
        """
        Führt SYNTEX-Kalibrierung durch.
        
        Args:
            meta_prompt: Der zu analysierende Meta-Prompt
            verbose: Ausgabe im Terminal
        
        Returns:
            (success, response, metadata)
        """
        # 1. Wrapper laden und Prompt bauen
        if verbose:
            print(f"🔧 Lade SYNTEX Framework...")
        
        try:
            full_prompt = self.wrapper.build_prompt(meta_prompt)
        except FileNotFoundError as e:
            print(f"❌ {e}")
            return False, None, {"error": str(e)}
        
        if verbose:
            print(f"📊 Meta-Prompt: {len(meta_prompt)} Zeichen")
            print(f"📊 Full Prompt: {len(full_prompt)} Zeichen")
            print(f"📤 Sende an 7B Model...")
        
        # 2. An 7B senden
        start_time = time.time()
        response, error, retry_count = self.client.send(full_prompt)
        duration_ms = int((time.time() - start_time) * 1000)
        
        # 3. Logging
        success = (error is None)
        
        self.logger.log_calibration(
            meta_prompt=meta_prompt,
            full_prompt=full_prompt,
            response=response,
            success=success,
            duration_ms=duration_ms,
            retry_count=retry_count,
            error=error,
            model_params=MODEL_PARAMS
        )
        
        # 4. Output
        if success:
            if verbose:
                print(f"✅ Kalibrierung erfolgreich ({duration_ms}ms, {retry_count + 1} Versuch(e))")
                print(f"\n{'='*80}")
                print(f"SYNTEX::CALIBRATION_RESPONSE")
                print(f"{'='*80}\n")
                print(response)
                print(f"\n{'='*80}\n")
        else:
            if verbose:
                print(f"❌ Kalibrierung fehlgeschlagen: {error}")
        
        metadata = {
            "duration_ms": duration_ms,
            "retry_count": retry_count,
            "error": error
        }
        
        return success, response, metadata
