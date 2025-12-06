"""
SYNTEX Quality Scoring System
Unterstützt Menschlich + SIGMA Terminologie
"""

from typing import Dict
from dataclasses import dataclass

from ..core.parser import SyntexFields


@dataclass
class QualityScore:
    """SYNTEX Quality Metrics"""
    total_score: int
    field_completeness: int
    structure_adherence: int
    detail_breakdown: Dict[str, bool]
    
    def to_dict(self) -> Dict:
        return {
            "total_score": self.total_score,
            "field_completeness": self.field_completeness,
            "structure_adherence": self.structure_adherence,
            "detail_breakdown": self.detail_breakdown
        }


class SyntexScorer:
    """Bewertet SYNTEX Response Quality (beide Terminologien)"""
    
    def __init__(self):
        # Menschliche Terminologie
        self.human_field_weights = {
            "drift": 15,
            "hintergrund_muster": 20,
            "druckfaktoren": 15,
            "tiefe": 20,
            "wirkung": 20,
            "klartext": 10
        }
        
        # SIGMA Terminologie
        self.sigma_field_weights = {
            "sigma_drift": 15,
            "sigma_mechanismus": 20,
            "sigma_frequenz": 15,
            "sigma_dichte": 20,
            "sigma_strome": 20,
            "sigma_extrakt": 10
        }
    
    def score(self, fields: SyntexFields, response_text: str) -> QualityScore:
        """Bewertet SYNTEX Quality - automatische Terminologie-Erkennung"""
        
        field_scores = {}
        total_field_score = 0
        
        # Erkenne welche Terminologie verwendet wurde
        is_sigma = fields.is_sigma()
        
        if is_sigma:
            # SIGMA Scoring
            weights = self.sigma_field_weights
            field_list = ["sigma_drift", "sigma_mechanismus", "sigma_frequenz", 
                         "sigma_dichte", "sigma_strome", "sigma_extrakt"]
        else:
            # Menschliche Terminologie Scoring
            weights = self.human_field_weights
            field_list = ["drift", "hintergrund_muster", "druckfaktoren", 
                         "tiefe", "wirkung", "klartext"]
        
        # Score Felder
        for field_name in field_list:
            weight = weights.get(field_name, 0)
            field_value = getattr(fields, field_name)
            has_content = field_value is not None and len(field_value.strip()) > 0
            field_scores[field_name] = has_content
            
            if has_content:
                total_field_score += weight
        
        field_completeness = total_field_score
        
        # Structure Adherence
        structure_score = 0
        required_markers = ["1.", "2.", "3.", "4.", "5.", "6."]
        for marker in required_markers:
            if marker in response_text:
                structure_score += 100 // len(required_markers)
        
        # Total Score
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
            field_display = field.upper().replace('_', ' ')
            output.append(f"   {icon} {field_display}")
        
        return "\n".join(output)
