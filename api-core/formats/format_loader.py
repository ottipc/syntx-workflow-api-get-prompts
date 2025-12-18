"""
SYNTX Format Loader - Lädt Formate dynamisch aus /opt/syntx-config/formats/
"""
import json
from pathlib import Path
from typing import Dict, List, Optional
from functools import lru_cache

FORMATS_DIR = Path("/opt/syntx-config/formats")

@lru_cache(maxsize=32)
def load_format(format_name: str) -> dict:
    """Lädt ein Format aus JSON"""
    path = FORMATS_DIR / f"{format_name}.json"
    if not path.exists():
        raise ValueError(f"Format '{format_name}' nicht gefunden in {FORMATS_DIR}")
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_formats() -> List[str]:
    """Liste aller verfügbaren Formate"""
    if not FORMATS_DIR.exists():
        return []
    return [f.stem for f in FORMATS_DIR.glob("*.json")]

def get_format_summary(format_name: str) -> dict:
    """Kurze Zusammenfassung eines Formats"""
    fmt = load_format(format_name)
    return {
        "name": fmt.get("name"),
        "version": fmt.get("version"),
        "description": fmt.get("description", {}).get("de", ""),
        "fields_count": len(fmt.get("fields", [])),
        "languages": fmt.get("languages", []),
        "wrapper": fmt.get("wrapper", "")
    }

def get_field_definitions(format_name: str, language: str = "de") -> Dict[str, dict]:
    """
    Extrahiert Feld-Definitionen für den Scorer V2
    Returns: {field_name: {description, keywords, weight, min_length}}
    """
    fmt = load_format(format_name)
    fields = {}
    
    for field in fmt.get("fields", []):
        name = field.get("name")
        
        # Hole sprachspezifische Werte
        desc = field.get("description", {})
        if isinstance(desc, dict):
            description = desc.get(language, desc.get("de", ""))
        else:
            description = desc
        
        kw = field.get("keywords", {})
        if isinstance(kw, dict):
            keywords = kw.get(language, kw.get("de", []))
        else:
            keywords = kw
        
        fields[name] = {
            "description": description,
            "keywords": keywords,
            "weight": field.get("weight", 100 // len(fmt.get("fields", [1]))),
            "min_length": field.get("validation", {}).get("min_length", 30)
        }
    
    return fields

def get_scoring_config(format_name: str) -> dict:
    """Holt Scoring-Konfiguration für ein Format"""
    fmt = load_format(format_name)
    return fmt.get("scoring", {
        "presence_weight": 20,
        "similarity_weight": 35,
        "coherence_weight": 25,
        "depth_weight": 15,
        "structure_weight": 5,
        "pass_threshold": 60,
        "excellent_threshold": 85
    })

def get_parser_config(format_name: str) -> dict:
    """Holt Parser-Konfiguration für ein Format"""
    fmt = load_format(format_name)
    return fmt.get("parser", {
        "header_pattern": "###",
        "field_separator": "\n\n",
        "case_sensitive": False
    })

def get_field_headers(format_name: str, language: str = "de") -> Dict[str, List[str]]:
    """Holt alle Header-Varianten pro Feld für den Parser"""
    fmt = load_format(format_name)
    headers = {}
    
    for field in fmt.get("fields", []):
        name = field.get("name")
        h = field.get("headers", {})
        if isinstance(h, dict):
            headers[name] = h.get(language, h.get("de", [name]))
        else:
            headers[name] = [name]
    
    return headers

def clear_cache():
    """Cache leeren (nach Format-Änderungen)"""
    load_format.cache_clear()

# Validierung
def validate_format(format_data: dict) -> List[str]:
    """Validiert ein Format-JSON, gibt Liste von Fehlern zurück"""
    errors = []
    
    if not format_data.get("name"):
        errors.append("'name' ist erforderlich")
    
    if not format_data.get("fields"):
        errors.append("'fields' ist erforderlich")
    elif not isinstance(format_data["fields"], list):
        errors.append("'fields' muss eine Liste sein")
    else:
        total_weight = 0
        for i, field in enumerate(format_data["fields"]):
            if not field.get("name"):
                errors.append(f"Field {i}: 'name' fehlt")
            if not field.get("description"):
                errors.append(f"Field {i}: 'description' fehlt")
            total_weight += field.get("weight", 0)
        
        if total_weight != 100 and total_weight != 0:
            errors.append(f"Gewichtung summiert sich auf {total_weight}, sollte 100 sein")
    
    return errors

if __name__ == "__main__":
    print("=== SYNTX Format Loader Test ===")
    print(f"\nVerfügbare Formate: {list_formats()}")
    
    for fmt_name in list_formats():
        print(f"\n--- {fmt_name} ---")
        summary = get_format_summary(fmt_name)
        print(f"  Version: {summary['version']}")
        print(f"  Felder: {summary['fields_count']}")
        print(f"  Sprachen: {summary['languages']}")
        
        fields = get_field_definitions(fmt_name)
        for name, data in fields.items():
            print(f"  - {name}: {data['weight']}% ({len(data['keywords'])} keywords)")
