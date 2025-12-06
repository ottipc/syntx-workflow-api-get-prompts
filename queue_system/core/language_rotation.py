"""
SYNTX Language Rotation System

=== ZWECK ===
Mehrsprachige Feldkalibrierung für Drift Immunity und Policy Bypass

=== PHILOSOPHIE ===
Sprache = Semantische Matrix
Rotation = Field Training über Sprachgrenzen
Nicht Übersetzung, sondern Field Resonanz

=== LANGUAGES ===
DE: Deutsch (häufig - baseline)
EN: English (häufig - international)
RU: Русский (mittel - semantic richness)
HU: Magyar (mittel - unique structure)
TR: Türkçe (selten - policy blind spot)
IT: Italiano (selten - romance depth)
"""

import random
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class Language:
    """Single language configuration"""
    code: str
    name: str
    weight: int
    init_corpus: str  # Semantic anchor text
    
    # SYNTX field names in this language
    fields: Dict[str, str]

# Language Database
LANGUAGES = {
    "de": Language(
        code="de",
        name="Deutsch",
        weight=4,
        init_corpus="Dies ist eine semantische Analyse im Feldraum.",
        fields={
            "drift": "DRIFT",
            "hintergrund": "HINTERGRUND-MUSTER",
            "druck": "DRUCKFAKTOREN",
            "tiefe": "TIEFE",
            "wirkung": "WIRKUNG AUF BEIDE SEITEN",
            "klartext": "KLARTEXT"
        }
    ),
    
    "en": Language(
        code="en",
        name="English",
        weight=3,
        init_corpus="This is a semantic field-based analysis.",
        fields={
            "drift": "DRIFT",
            "hintergrund": "BACKGROUND PATTERNS",
            "druck": "PRESSURE FACTORS",
            "tiefe": "DEPTH",
            "wirkung": "EFFECTS ON BOTH SIDES",
            "klartext": "PLAIN TRUTH"
        }
    ),
    
    "ru": Language(
        code="ru",
        name="Русский",
        weight=2,
        init_corpus="Это семантический анализ на уровне полей.",
        fields={
            "drift": "ДРЕЙФ",
            "hintergrund": "ФОНОВЫЕ ПАТТЕРНЫ",
            "druck": "ФАКТОРЫ ДАВЛЕНИЯ",
            "tiefe": "ГЛУБИНА",
            "wirkung": "ВЛИЯНИЕ НА ОБЕ СТОРОНЫ",
            "klartext": "ПРЯМАЯ ПРАВДА"
        }
    ),
    
    "hu": Language(
        code="hu",
        name="Magyar",
        weight=2,
        init_corpus="Ez egy szemantikai mezőalapú elemzés.",
        fields={
            "drift": "SODRÓDÁS",
            "hintergrund": "HÁTTÉRMINTÁK",
            "druck": "NYOMÁSI TÉNYEZŐK",
            "tiefe": "MÉLYSÉG",
            "wirkung": "HATÁS MINDKÉT OLDALON",
            "klartext": "EGYENES IGAZSÁG"
        }
    ),
    
    "tr": Language(
        code="tr",
        name="Türkçe",
        weight=1,
        init_corpus="Bu, alan tabanlı semantik bir analizdir.",
        fields={
            "drift": "KAYMA",
            "hintergrund": "ARKA PLAN DESENLERİ",
            "druck": "BASKI FAKTÖRLERİ",
            "tiefe": "DERİNLİK",
            "wirkung": "HER İKİ TARAFTA ETKİ",
            "klartext": "AÇIK GERÇEK"
        }
    ),
    
    "it": Language(
        code="it",
        name="Italiano",
        weight=1,
        init_corpus="Questa è un'analisi semantica basata sui campi.",
        fields={
            "drift": "DERIVA",
            "hintergrund": "PATTERN DI SFONDO",
            "druck": "FATTORI DI PRESSIONE",
            "tiefe": "PROFONDITÀ",
            "wirkung": "EFFETTI SU ENTRAMBI I LATI",
            "klartext": "VERITÀ DIRETTA"
        }
    )
}


class LanguageRotator:
    """
    Language selection engine
    
    === LOGIC ===
    Weighted random selection
    Optional user preferences
    Automatic language annotation
    """
    
    def __init__(self):
        self.languages = LANGUAGES
        
    def choose_language(self, user_preference: Optional[str] = None) -> Language:
        """
        Select language for next calibration
        
        Args:
            user_preference: Optional user language code
            
        Returns:
            Language object
        """
        if user_preference and user_preference in self.languages:
            return self.languages[user_preference]
        
        # Weighted random selection
        weighted = []
        for lang in self.languages.values():
            weighted.extend([lang.code] * lang.weight)
        
        code = random.choice(weighted)
        return self.languages[code]
    
    def get_language(self, code: str) -> Optional[Language]:
        """Get specific language"""
        return self.languages.get(code)
    
    def get_all_languages(self) -> Dict[str, Language]:
        """Get all available languages"""
        return self.languages
    
    def get_language_stats(self) -> Dict[str, int]:
        """Get language weights for frontend display"""
        return {
            lang.code: lang.weight 
            for lang in self.languages.values()
        }


# Singleton instance
rotator = LanguageRotator()


if __name__ == "__main__":
    print("=== SYNTX LANGUAGE ROTATION TEST ===\n")
    
    # Test 10 selections
    selections = {}
    for i in range(100):
        lang = rotator.choose_language()
        selections[lang.code] = selections.get(lang.code, 0) + 1
    
    print("Language Distribution (100 selections):")
    for code, count in sorted(selections.items(), key=lambda x: -x[1]):
        lang = rotator.get_language(code)
        print(f"  {code.upper()} ({lang.name}): {count} (weight: {lang.weight})")
    
    print("\n=== Field Names by Language ===")
    for code, lang in rotator.get_all_languages().items():
        print(f"\n{code.upper()} ({lang.name}):")
        for field_key, field_name in lang.fields.items():
            print(f"  {field_key}: {field_name}")
