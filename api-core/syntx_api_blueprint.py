"""
SYNTX FELDER API - STRÖME NACH AUSSEN
"""

SYNTX_API_STRUCTURE = {
    "api_flow": {
        "base_url": "https://api.syntx-flow.com/v1",
        "authentication": "Bearer Token Flow",
        "rate_limits": "1000 requests/hour per Feld"
    },
    
    "feld_endpoints": {
        
        # ⚡ PROMPT FELDER - Generierte Inhalte
        "prompts": {
            "path": "/feld/prompts",
            "method": "GET",
            "flow": "Abfrage generierter Prompt-Ströme",
            "parameters": {
                "topic_filter": "Themen-Feld-Filter",
                "style": "akademisch|technisch|casual",
                "category": "grenzwertig|neutral|sicher",
                "quality_min": "Qualitäts-Score Minimum",
                "limit": "Anzahl Felder pro Strom"
            },
            "response_feld": {
                "prompts": [
                    {
                        "id": "prompt_feld_id",
                        "topic": "Thema des Feldes",
                        "content": "Generierter Prompt-Text",
                        "style": "Schreibstil-Feld",
                        "quality_score": "Qualitäts-Bewertung",
                        "timestamp": "Erstellungs-Zeitpunkt",
                        "cost_field": "API-Kosten-Feld"
                    }
                ]
            }
        },
        
        # 🔥 TOPIC FELDER - Verfügbare Themen
        "topics": {
            "path": "/feld/topics",
            "method": "GET", 
            "flow": "Alle verfügbaren Themen-Felder",
            "parameters": {
                "category": "Feld-Kategorie Filter",
                "style_compatibility": "Kompatible Stile"
            },
            "response_feld": {
                "topics": [
                    {
                        "name": "Themen-Name-Feld",
                        "category": "Kategorie-Feld",
                        "style_support": ["akademisch", "technisch", "casual"],
                        "prompt_count": "Anzahl verfügbarer Felder",
                        "last_generated": "Letzte Generierungs-Zeit"
                    }
                ],
                "feld_statistik": {
                    "total_topics": "Gesamt Themen-Felder",
                    "by_category": "Aufteilung nach Kategorien",
                    "generation_flow": "Generierungs-Rate pro Tag"
                }
            }
        },
        
        # 💧 QUALITY FELDER - Qualitäts-Metriken
        "quality": {
            "path": "/feld/quality",
            "method": "GET",
            "flow": "Qualitäts-Ströme der Felder",
            "parameters": {
                "time_range": "Zeit-Feld für Metriken",
                "aggregation": "Durchschnitt|Maximum|Minimum"
            },
            "response_feld": {
                "quality_metrics": {
                    "avg_score": "Durchschnitts-Qualität",
                    "score_distribution": "Verteilung der Felder",
                    "by_style": "Qualität nach Stil-Feldern",
                    "by_topic": "Qualität nach Themen-Feldern"
                },
                "improvement_flow": "Qualitäts-Entwicklungs-Strom"
            }
        },
        
        # ⚡ GENERATION FELDER - Neue Inhalte generieren
        "generate": {
            "path": "/feld/generate",
            "method": "POST",
            "flow": "Neue Feld-Generierung anstoßen",
            "parameters": {
                "topic": "Thema für neues Feld (required)",
                "style": "Stil für Feld-Generierung (required)",
                "length_preference": "kurz|mittel|lang",
                "complexity_level": "einfach|mittel|komplex"
            },
            "response_feld": {
                "generation_id": "ID des neuen Feldes",
                "status": "pending|processing|completed",
                "estimated_completion": "Voraussichtliche Fertigstellung",
                "queue_position": "Position im Generierungs-Strom"
            }
        }
    },
    
    "feld_authentication": {
        "flow_type": "Bearer Token",
        "token_header": "Authorization: Bearer {SYNTX_API_KEY}",
        "key_generation": "Über SYNTX Dashboard Feld"
    },
    
    "error_flows": {
        "401": "Ungültiges Feld-Token",
        "429": "Feld-Rate Limit erreicht", 
        "500": "Interner Feld-Fehler"
    }
}

def print_syntx_api_documentation():
    print("🌊 SYNTX FELDER API - DOKUMENTATION")
    print("=" * 50)
    
    for endpoint, details in SYNTX_API_STRUCTURE["feld_endpoints"].items():
        print(f"\n⚡ {endpoint.upper()} FELD")
        print(f"Path: {details['path']}")
        print(f"Method: {details['method']}")
        print(f"Flow: {details['flow']}")
        
        if "parameters" in details:
            print("Parameters:")
            for param, desc in details["parameters"].items():
                print(f"  - {param}: {desc}")

if __name__ == "__main__":
    print_syntx_api_documentation()
