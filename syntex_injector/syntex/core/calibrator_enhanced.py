"""
Enhanced SYNTEX Calibration Engine
Mit Parser, Scorer und Progress Tracking
"""

import time
import uuid
from pathlib import Path
from typing import Optional, Tuple, Dict

from .wrapper import SyntexWrapper
from .logger import CalibrationLogger
from .parser import SyntexParser
from ..api.client import APIClient
from ..api.config import MODEL_PARAMS
from ..analysis.scorer import SyntexScorer
from ..analysis.tracker import ProgressTracker


class EnhancedSyntexCalibrator:
    """
    Enhanced SYNTEX::TRUE_RAW Kalibrierungs-Engine
    
    Features:
    - Response Parsing
    - Quality Scoring
    - Progress Tracking
    - Detailed Logging
    """
    
    def __init__(
        self,
        wrapper_name: str = "human",
        log_file: Optional[Path] = None,
        progress_file: Optional[Path] = None
    ):
        self.wrapper = SyntexWrapper(wrapper_name)
        self.client = APIClient()
        self.logger = CalibrationLogger(log_file)
        self.parser = SyntexParser()
        self.scorer = SyntexScorer()
        self.tracker = ProgressTracker(progress_file)
        self.session_id = str(uuid.uuid4())[:8]
    
    def calibrate(
        self,
        meta_prompt: str,
        verbose: bool = True,
        show_quality: bool = True
    ) -> Tuple[bool, Optional[str], Dict]:
        """
        Führt Enhanced SYNTEX-Kalibrierung durch.
        
        Args:
            meta_prompt: Der zu analysierende Meta-Prompt
            verbose: Ausgabe im Terminal
            show_quality: Zeige Quality Score
        
        Returns:
            (success, response, metadata)
        """
        # 1. Wrapper laden und Prompt bauen
        if verbose:
            print(f"🔧 SYNTEX Framework laden...")
        
        try:
            full_prompt = self.wrapper.build_prompt(meta_prompt)
        except FileNotFoundError as e:
            print(f"❌ {e}")
            return False, None, {"error": str(e)}
        
        if verbose:
            print(f"📊 Meta-Prompt: {len(meta_prompt)} Zeichen")
            print(f"📊 Full Prompt: {len(full_prompt)} Zeichen")
            print(f"📤 Sende an Model (Session: {self.session_id})...")
        
        # 2. An Model senden
        start_time = time.time()
        response, error, retry_count = self.client.send(full_prompt)
        duration_ms = int((time.time() - start_time) * 1000)
        
        success = (error is None)
        
        # 3. Response analysieren
        quality_score = None
        parsed_fields = None
        
        if success and response:
            try:
                # Parse SYNTEX Fields
                parsed_fields = self.parser.parse(response)
                
                # Score Quality
                quality_score = self.scorer.score(parsed_fields, response)
                
                # Track Progress
                self.tracker.log_progress(
                    session_id=self.session_id,
                    score=quality_score,
                    meta_prompt_length=len(meta_prompt)
                )
                
            except Exception as parse_error:
                if verbose:
                    print(f"⚠️  Parse/Score Error: {parse_error}")
        
        # 4. Logging
        log_data = {
            "meta_prompt": meta_prompt,
            "full_prompt": full_prompt,
            "response": response,
            "success": success,
            "duration_ms": duration_ms,
            "retry_count": retry_count,
            "error": error,
            "model_params": MODEL_PARAMS
        }
        
        if quality_score:
            log_data["quality_score"] = quality_score.to_dict()
        
        if parsed_fields:
            log_data["parsed_fields"] = parsed_fields.to_dict()
        
        self.logger.log_calibration(**log_data)
        
        # 5. Output
        if success:
            if verbose:
                print(f"✅ Kalibrierung erfolgreich ({duration_ms}ms, {retry_count + 1} Versuch(e))")
                
                if show_quality and quality_score:
                    print(self.scorer.format_score_output(quality_score))
                
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
            "error": error,
            "quality_score": quality_score.to_dict() if quality_score else None,
            "session_id": self.session_id
        }
        
        return success, response, metadata
