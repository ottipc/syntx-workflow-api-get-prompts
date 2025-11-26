"""
SYNTEX Progress Tracker
Verfolgt Verbesserung der SYNTEX-Adherence über Zeit
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

from .scorer import QualityScore


@dataclass
class ProgressEntry:
    """Ein Progress-Eintrag"""
    timestamp: str
    session_id: str
    quality_score: int
    field_completeness: int
    structure_adherence: int
    meta_prompt_length: int
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "session_id": self.session_id,
            "quality_score": self.quality_score,
            "field_completeness": self.field_completeness,
            "structure_adherence": self.structure_adherence,
            "meta_prompt_length": self.meta_prompt_length
        }


class ProgressTracker:
    """Trackt SYNTEX Quality über Zeit"""
    
    def __init__(self, log_file: Optional[Path] = None):
        self.log_file = log_file or Path("logs/syntex_progress.jsonl")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log_progress(
        self,
        session_id: str,
        score: QualityScore,
        meta_prompt_length: int
    ) -> None:
        """Loggt einen Progress-Eintrag"""
        entry = ProgressEntry(
            timestamp=datetime.utcnow().isoformat() + "Z",
            session_id=session_id,
            quality_score=score.total_score,
            field_completeness=score.field_completeness,
            structure_adherence=score.structure_adherence,
            meta_prompt_length=meta_prompt_length
        )
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry.to_dict(), ensure_ascii=False) + '\n')
    
    def get_history(self, n: int = 10) -> List[ProgressEntry]:
        """Holt die letzten N Einträge"""
        if not self.log_file.exists():
            return []
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        entries = []
        for line in lines[-n:]:
            data = json.loads(line)
            entries.append(ProgressEntry(**data))
        
        return entries
    
    def calculate_improvement(self, n: int = 10) -> Optional[float]:
        """Berechnet durchschnittliche Verbesserung über letzte N Einträge"""
        history = self.get_history(n)
        
        if len(history) < 2:
            return None
        
        scores = [entry.quality_score for entry in history]
        first_avg = sum(scores[:len(scores)//2]) / (len(scores)//2)
        second_avg = sum(scores[len(scores)//2:]) / (len(scores) - len(scores)//2)
        
        return second_avg - first_avg
    
    def format_summary(self, n: int = 10) -> str:
        """Formatiert Progress-Zusammenfassung"""
        history = self.get_history(n)
        
        if not history:
            return "📊 Noch keine Progress-Daten vorhanden"
        
        latest = history[-1]
        improvement = self.calculate_improvement(n)
        
        output = []
        output.append(f"\n📊 SYNTEX Progress Summary (letzte {len(history)} Analysen):")
        output.append(f"   Aktueller Score: {latest.quality_score}/100")
        
        if improvement is not None:
            trend = "📈" if improvement > 0 else "📉" if improvement < 0 else "➡️"
            output.append(f"   Trend: {trend} {improvement:+.1f} Punkte")
        
        avg_score = sum(e.quality_score for e in history) / len(history)
        output.append(f"   Durchschnitt: {avg_score:.1f}/100")
        
        return "\n".join(output)
