"""
SYNTEX Quality Scoring System
Bewertet wie gut Model-Responses dem SYNTEX Framework folgen
"""

from typing import Dict
from dataclasses import dataclass

from ..core.parser import SyntexFields


@dataclass
class QualityScore:
    """SYNTEX Quality Metrics"""
    total_score: int  # 0-100
    field_completeness: int  # 0-100
    structure_adherence: int  # 0-100
    detail_breakdown: Dict[str, bool]
    
    def to_dict(self) -> Dict:
        return {
            "total_score": self.total_score,
            "field_completeness": self.field_completeness,
            "structure_adherence": self.structure_adherence,
            "detail_breakdown": self.detail_breakdown
        }


class SyntexScorer:
    """Bewertet SYNTEX Response Quality"""
    
    def __init__(self):
        self.field_weights = {
            "drift": 15,
            "hintergrund_muster": 20,
            "druckfaktoren": 15,
            "tiefe": 20,
            "wirkung": 20,
            "klartext": 10
        }
    
    def score(self, fields: SyntexFields, response_text: str) -> QualityScore:
        """
        Bewertet SYNTEX Quality.
        
        Args:
            fields: Geparste SyntexFields
            response_text: Original Response
        
        Returns:
            QualityScore mit Metriken
        """
        # Field Completeness Score
        field_scores = {}
        total_field_score = 0
        
        for field_name, weight in self.field_weights.items():
            field_value = getattr(fields, field_name)
            has_content = field_value is not None and len(field_value.strip()) > 0
            field_scores[field_name] = has_content
            
            if has_content:
                total_field_score += weight
        
        field_completeness = total_field_score
        
        # Structure Adherence (prüft ob nummerierte Struktur vorhanden)
        structure_score = 0
        required_markers = ["1.", "2.", "3.", "4.", "5.", "6."]
        for marker in required_markers:
            if marker in response_text:
                structure_score += 100 // len(required_markers)
        
        # Total Score (gewichteter Durchschnitt)
        total_score = int((field_completeness * 0.7) + (structure_score * 0.3))
        
        return QualityScore(
            total_score=total_score,
            field_completeness=field_completeness,
            structure_adherence=structure_score,
            detail_breakdown=field_scores
        )
    
    def format_score_output(self, score: QualityScore) -> str:
        """Formatiert Score für Terminal-Ausgabe"""
        output = []
        output.append(f"\n📊 SYNTEX Quality Score: {score.total_score}/100")
        output.append(f"   Field Completeness: {score.field_completeness}/100")
        output.append(f"   Structure Adherence: {score.structure_adherence}/100")
        output.append("\nField Breakdown:")
        
        for field, present in score.detail_breakdown.items():
            icon = "✅" if present else "❌"
            output.append(f"   {icon} {field.upper()}")
        
        return "\n".join(output)
