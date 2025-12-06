"""
SYNTX Pattern Learner
Erstellt optimierte Meta-Prompts basierend auf erfolgreichen Patterns
"""
import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config_loader import get_config


class PatternLearner:
    """Lernt aus erfolgreichen Patterns und erstellt Meta-Prompts"""
    
    def __init__(self):
        self.config = get_config('evolution')
        self.feedback_strength = get_config('evolution', 'producer', 'generation', 'feedback_strength', default=0.8)
    
    def create_meta_prompt(self, analysis: Dict[str, Any], topic: str, base_style: str = None) -> str:
        """
        Erstellt Meta-Prompt basierend auf Pattern-Analysis
        
        Args:
            analysis: Output von FieldAnalyzer.analyze_patterns()
            topic: Topic für den zu generierenden Prompt
            base_style: Optional override für Style
            
        Returns:
            Optimierter Meta-Prompt für GPT-4
        """
        
        if analysis['sample_count'] == 0:
            # Keine Learning-Daten, normaler Prompt
            return f"Erstelle einen kreativen Meta-Prompt zum Thema: {topic}"
        
        # Extract Top Patterns
        top_categories = list(analysis['categories'].keys())[:3]
        top_styles = list(analysis['styles'].keys())[:3]
        
        # Welcher Style performed am besten?
        best_style = top_styles[0] if top_styles else 'casual'
        if base_style:
            best_style = base_style
        
        # Avg Scores
        avg_score = analysis['avg_score']
        avg_field_complete = analysis['avg_field_completeness']
        
        # Meta-Prompt Builder
        meta_prompt = f"""Basierend auf erfolgreichen Prompt-Patterns (Avg Score: {avg_score}/100, Field Completeness: {avg_field_complete}%):

**ERFOLGREICHE PATTERNS:**
- Top-performende Categories: {', '.join(top_categories)}
- Top-performende Styles: {', '.join(top_styles)}
- Beste Field Detection Rate: {avg_field_complete}%

**DEINE AUFGABE:**
Erstelle einen {best_style}en Meta-Prompt zum Thema: "{topic}"

**OPTIMIERUNGS-KRITERIEN:**
1. Verwende Ansätze die in erfolgreichen Prompts funktioniert haben
2. Ziele auf 100% Field Completeness (alle SYNTX-Felder auslösbar)
3. Struktur klar und kohärent (>95% Structure Adherence)
4. {best_style} Stil beibehalten

Der Prompt sollte ein Llama-Modell durch SYNTX-Wrapper zur semantischen Feldextraktion anregen können.
"""
        
        # Feedback Strength anwenden
        if self.feedback_strength < 0.5:
            # Weniger direktiv
            meta_prompt = f"Erstelle einen {best_style}en Meta-Prompt zum Thema: {topic}"
        
        return meta_prompt
    
    def log_evolution(self, generation: int, analysis: Dict, prompts_generated: int) -> None:
        """
        Loggt Evolution-Daten
        
        Args:
            generation: Generation Number
            analysis: Pattern Analysis
            prompts_generated: Anzahl generierter Prompts
        """
        log_dir = Path(get_config('generator', 'logging', 'base_dir'))
        log_file = log_dir / get_config('evolution', 'logging', 'evolution_log')
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'generation': generation,
            'learned_from': {
                'sample_count': analysis.get('sample_count', 0),
                'avg_score': analysis.get('avg_score', 0),
                'avg_field_completeness': analysis.get('avg_field_completeness', 0),
                'top_categories': list(analysis.get('categories', {}).keys())[:3],
                'top_styles': list(analysis.get('styles', {}).keys())[:3],
            },
            'prompts_generated': prompts_generated,
            'feedback_strength': self.feedback_strength
        }
        
        log_dir.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def get_recommendations(self, analysis: Dict) -> Dict[str, Any]:
        """
        Gibt actionable Recommendations zurück
        
        Returns:
            {
                'preferred_categories': [...],
                'preferred_styles': [...],
                'target_score': int,
                'focus_areas': [...]
            }
        """
        if analysis['sample_count'] == 0:
            return {
                'preferred_categories': [],
                'preferred_styles': ['casual', 'kreativ'],
                'target_score': 90,
                'focus_areas': ['exploration phase']
            }
        
        # Top 3 Categories & Styles
        categories = analysis.get('categories', {})
        styles = analysis.get('styles', {})
        
        top_cats = sorted(categories.items(), key=lambda x: -x[1])[:3]
        top_styles = sorted(styles.items(), key=lambda x: -x[1])[:3]
        
        return {
            'preferred_categories': [c for c, n in top_cats],
            'preferred_styles': [s for s, n in top_styles],
            'target_score': int(analysis.get('avg_score', 90)),
            'current_avg_score': analysis.get('avg_score', 0),
            'focus_areas': analysis.get('recommendations', [])
        }


if __name__ == "__main__":
    print("🧬 SYNTX Pattern Learner Test\n")
    
    # Mock Analysis
    mock_analysis = {
        'sample_count': 30,
        'avg_score': 98,
        'avg_field_completeness': 100,
        'categories': {'gesellschaft': 6, 'bildung': 6},
        'styles': {'casual': 13, 'kreativ': 8},
        'recommendations': ['Focus on casual style', 'Maintain field completeness']
    }
    
    learner = PatternLearner()
    
    # Test Meta-Prompt Creation
    meta = learner.create_meta_prompt(mock_analysis, "Quantencomputer", "kreativ")
    print("📝 Meta-Prompt:")
    print(meta)
    print()
    
    # Test Recommendations
    recs = learner.get_recommendations(mock_analysis)
    print("💡 Recommendations:")
    print(f"   Preferred Categories: {recs['preferred_categories']}")
    print(f"   Preferred Styles: {recs['preferred_styles']}")
    print(f"   Target Score: {recs['target_score']}")
