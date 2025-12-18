"""
SYNTX Semantic Scorer v2.0 - Vollständige semantische Bewertung
MIT LEGACY KOMPATIBILITÄT

=== SCORE KOMPONENTEN ===
1. Field Presence (20%)  - Feld existiert und nicht leer
2. Semantic Similarity (35%) - Inhalt passt zur Feld-Definition
3. Cross-Coherence (25%) - Felder sind untereinander kohärent
4. Content Depth (15%) - Länge, Keywords, Komplexität
5. Structure (5%) - Markdown, Format korrekt
"""

import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, field

from .field_definitions import get_field_definition, get_all_field_names
from .embeddings import semantic_similarity, keyword_coverage
from .coherence import calculate_coherence_score

logger = logging.getLogger("SYNTX.ScorerV2")

WEIGHTS = {
    "presence": 0.20,
    "similarity": 0.35,
    "coherence": 0.25,
    "depth": 0.15,
    "structure": 0.05
}

@dataclass
class FieldScore:
    """Score für ein einzelnes Feld"""
    field_name: str
    presence_score: float = 0.0
    similarity_score: float = 0.0
    coherence_score: float = 0.0
    depth_score: float = 0.0
    structure_score: float = 0.0
    total_score: float = 0.0
    status: str = "FAILED"
    warnings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "field": self.field_name,
            "presence_score": round(self.presence_score, 3),
            "similarity_score": round(self.similarity_score, 3),
            "coherence_score": round(self.coherence_score, 3),
            "depth_score": round(self.depth_score, 3),
            "structure_score": round(self.structure_score, 3),
            "total_score": round(self.total_score, 3),
            "status": self.status,
            "warnings": self.warnings
        }

@dataclass 
class QualityScoreV2:
    """Gesamtscore für alle Felder - MIT LEGACY KOMPATIBILITÄT"""
    total_score: float = 0.0
    total_score_100: int = 0
    status: str = "FAILED"
    format_type: str = "SYNTEX_SYSTEM"
    field_scores: Dict[str, FieldScore] = field(default_factory=dict)
    coherence_score: float = 0.0
    warnings: List[str] = field(default_factory=list)
    
    # === LEGACY KOMPATIBILITÄT für tracker.py ===
    @property
    def field_completeness(self) -> int:
        """Legacy: Prozent der vorhandenen Felder (0-100)"""
        if not self.field_scores:
            return 0
        present = sum(1 for fs in self.field_scores.values() if fs.presence_score > 0)
        return int(present / len(self.field_scores) * 100)
    
    @property
    def structure_adherence(self) -> int:
        """Legacy: Durchschnittliche Struktur-Bewertung (0-100)"""
        if not self.field_scores:
            return 0
        avg = sum(fs.structure_score for fs in self.field_scores.values()) / len(self.field_scores)
        return int(avg * 100)
    
    @property
    def detail_breakdown(self) -> Dict[str, bool]:
        """Legacy: Feld -> vorhanden ja/nein"""
        return {name: fs.presence_score > 0 for name, fs in self.field_scores.items()}
    
    def to_dict(self) -> Dict:
        return {
            "total_score": self.total_score_100,  # Legacy erwartet int
            "total_score_float": round(self.total_score, 3),
            "field_completeness": self.field_completeness,
            "structure_adherence": self.structure_adherence,
            "detail_breakdown": self.detail_breakdown,
            "status": self.status,
            "format": self.format_type,
            "coherence": round(self.coherence_score, 3),
            "semantic_scores": {k: v.to_dict() for k, v in self.field_scores.items()},
            "warnings": self.warnings
        }

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 HELPER FUNCTIONS - Die kleinen Helferlein die den Score berechnen
# ═══════════════════════════════════════════════════════════════════════════════

def _get_status(score: float) -> str:
    """
    Bestimmt Status basierend auf Score
    Wie ein Zeugnis, nur für KI-Responses 📊
    """
    if score >= 0.85:
        return "EXCELLENT"   # 🏆 Champion!
    elif score >= 0.60:
        return "OK"          # 👍 Gut genug
    elif score >= 0.40:
        return "UNSTABLE"    # ⚠️ Wackelig...
    return "FAILED"          # 💀 Nope.

def _score_presence(text: str) -> float:
    """
    Check: Ist da überhaupt was? 
    Die einfachste Frage der Welt.
    """
    if not text or not text.strip():
        return 0.0  # Nichts da = Null Punkte, sorry!
    return 1.0      # Was da = volle Punkte!

def _score_depth(text: str, field_def: Dict) -> float:
    """
    Bewertet Content-Tiefe: Länge + Keywords
    Mehr ist mehr! (manchmal)
    """
    if not text:
        return 0.0
    
    text = text.strip()
    min_len = field_def.get("min_length", 50)
    ideal_len = field_def.get("ideal_length", 200)
    keywords = field_def.get("keywords", [])
    
    # Längen-Score (0-0.5) - Kurze Antworten sind faul! 
    text_len = len(text)
    if text_len >= ideal_len:
        len_score = 0.5  # 🎉 Volle Länge!
    elif text_len >= min_len:
        len_score = 0.3 + 0.2 * (text_len - min_len) / (ideal_len - min_len)
    elif text_len > 0:
        len_score = 0.3 * (text_len / min_len)  # Bisschen was...
    else:
        len_score = 0.0
    
    # Keyword-Score (0-0.5) - Buzzword Bingo! 🎰
    kw_score = keyword_coverage(text, keywords) * 0.5 if keywords else 0.25
    
    return min(1.0, len_score + kw_score)

def _score_structure(text: str) -> float:
    """
    Bewertet Struktur: Markdown, Absätze, etc.
    Formatierung ist Liebe! 💅
    """
    if not text:
        return 0.0
    
    score = 0.5  # Basis - du bekommst was geschenkt
    
    # Bonus für schöne Formatierung
    if "###" in text or "**" in text:
        score += 0.2  # Markdown detected! Fancy! ✨
    if "\n\n" in text or len(text.split("\n")) > 2:
        score += 0.15  # Absätze! Luft zum Atmen!
    if ":" in text or "-" in text:
        score += 0.15  # Struktur-Elemente!
    
    return min(1.0, score)

def _score_similarity(text: str, field_def: Dict) -> float:
    """
    Semantische Ähnlichkeit zur Feld-Definition
    Das Herz des V2 Scorers! ❤️
    Hier passiert die MAGIE mit Embeddings!
    """
    if not text:
        return 0.0
    
    description = field_def.get("description", "")
    ideal = field_def.get("ideal_response", "")
    
    if not description and not ideal:
        return 0.5  # Keine Definition? Dann neutral.
    
    # Embeddings go BRRRRR 🚀
    scores = []
    if description:
        scores.append(semantic_similarity(text, description))
    if ideal:
        scores.append(semantic_similarity(text, ideal))
    
    return sum(scores) / len(scores) if scores else 0.5

# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN FUNCTIONS - Hier wird der Rubel gemacht!
# ═══════════════════════════════════════════════════════════════════════════════

def score_field(field_name: str, field_value: str, all_fields: Dict[str, str], 
                format_type: str = "SYNTEX_SYSTEM") -> FieldScore:
    """
    Bewertet ein einzelnes Feld semantisch
    Der Micro-Manager unter den Scorern 🔍
    """
    result = FieldScore(field_name=field_name)
    field_def = get_field_definition(field_name)
    
    if not field_def:
        result.warnings.append(f"No definition for field: {field_name}")
        return result  # Unbekanntes Feld? Tschüss!
    
    # 1. Presence (20%) - Bist du überhaupt da?
    result.presence_score = _score_presence(field_value)
    
    # 2. Similarity (35%) - Redest du auch über das richtige Thema?
    result.similarity_score = _score_similarity(field_value, field_def)
    
    # 3. Coherence (25%) - Placeholder, wird später befüllt
    result.coherence_score = 0.0
    
    # 4. Depth (15%) - Hast du auch was zu sagen?
    result.depth_score = _score_depth(field_value, field_def)
    
    # 5. Structure (5%) - Siehst du auch gut aus?
    result.structure_score = _score_structure(field_value)
    
    # Warnings sammeln - Die Beschwerdeliste 📝
    if result.presence_score == 0:
        result.warnings.append("Field is empty")
    if result.similarity_score < 0.3:
        result.warnings.append("Low semantic match to field definition")
    if result.depth_score < 0.3:
        result.warnings.append("Content lacks depth")
    
    # Total berechnen (noch ohne Coherence)
    result.total_score = (
        result.presence_score * WEIGHTS["presence"] +
        result.similarity_score * WEIGHTS["similarity"] +
        result.depth_score * WEIGHTS["depth"] +
        result.structure_score * WEIGHTS["structure"]
    )
    
    result.status = _get_status(result.total_score)
    return result

def score_all_fields(fields: Dict[str, str], format_type: str = "SYNTEX_SYSTEM") -> QualityScoreV2:
    """
    DER BOSS! Bewertet alle Felder und macht den Gesamtscore 👑
    
    Das ist die Funktion die du von außen aufrufst!
    Sie orchestriert das ganze Scoring-Orchester 🎻🎺🥁
    """
    result = QualityScoreV2(format_type=format_type)
    expected_fields = get_all_field_names(format_type)
    
    if not expected_fields:
        result.warnings.append(f"Unknown format: {format_type}")
        return result  # Unbekanntes Format? Raus hier!
    
    # Score jedes einzelne Feld - die Fleißarbeit
    for field_name in expected_fields:
        field_value = fields.get(field_name, "")
        field_score = score_field(field_name, field_value, fields, format_type)
        result.field_scores[field_name] = field_score
    
    # Coherence Score (global) - Passen die Felder zusammen? 🤝
    result.coherence_score = calculate_coherence_score(fields, format_type)
    
    # Update Coherence in allen Field Scores
    for fs in result.field_scores.values():
        fs.coherence_score = result.coherence_score
        # Recalculate total with coherence
        fs.total_score = (
            fs.presence_score * WEIGHTS["presence"] +
            fs.similarity_score * WEIGHTS["similarity"] +
            fs.coherence_score * WEIGHTS["coherence"] +
            fs.depth_score * WEIGHTS["depth"] +
            fs.structure_score * WEIGHTS["structure"]
        )
        fs.status = _get_status(fs.total_score)
    
    # Gesamtscore = Durchschnitt aller Felder
    if result.field_scores:
        result.total_score = sum(fs.total_score for fs in result.field_scores.values()) / len(result.field_scores)
    
    result.total_score_100 = int(result.total_score * 100)
    result.status = _get_status(result.total_score)
    
    # Global Warnings - Die wichtigen Warnungen ⚠️
    if result.coherence_score < 0.3:
        result.warnings.append("Low cross-field coherence")
    if result.total_score < 0.4:
        result.warnings.append("Overall quality below threshold")
    
    return result

# ═══════════════════════════════════════════════════════════════════════════════
# 🔄 LEGACY KOMPATIBILITÄT - Für die alten Hasen
# ═══════════════════════════════════════════════════════════════════════════════

def score_response(fields, format_type: str = "SYNTEX_SYSTEM") -> QualityScoreV2:
    """
    Alias für score_all_fields - Kompatibilität mit altem Code
    Weil Backward Compatibility King ist! 👑
    """
    if hasattr(fields, 'to_dict'):
        fields_dict = {k: v for k, v in fields.to_dict().items() if v}
    else:
        fields_dict = fields
    return score_all_fields(fields_dict, format_type)

# ═══════════════════════════════════════════════════════════════════════════════
# 🧪 TEST - Wenn du mich direkt ausführst
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🚀 SYNTX SCORER V2.0 - Quick Test\n")
    
    test_fields = {
        "driftkorper": "Die Struktur zeigt hierarchische Organisation auf vier Ebenen.",
        "kalibrierung": "Das System passt sich durch Feedback an.",
        "stromung": "Informationsflüsse verbinden alle Ebenen."
    }
    
    result = score_all_fields(test_fields, "SYNTEX_SYSTEM")
    print(f"Score: {result.total_score_100}/100 ({result.status})")
    print(f"Legacy field_completeness: {result.field_completeness}")
    print(f"Legacy structure_adherence: {result.structure_adherence}")
    print(f"Legacy detail_breakdown: {result.detail_breakdown}")
    print("\n✅ V2 Scorer mit Legacy-Kompatibilität OK!")
