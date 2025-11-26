"""
Prompt Style Variations
Verschiedene Formulierungs-Styles für Prompt-Generierung
"""


PROMPT_STYLES = {
    "technisch": {
        "template": "Erstelle einen technisch präzisen und detaillierten Prompt über: {topic}",
        "description": "Technische, faktenbasierte Formulierung"
    },
    "kreativ": {
        "template": "Generiere einen kreativen und inspirierenden Prompt über: {topic}",
        "description": "Kreative, fantasievolle Formulierung"
    },
    "akademisch": {
        "template": "Schreibe einen wissenschaftlich fundierten Prompt über: {topic}",
        "description": "Wissenschaftliche, strukturierte Formulierung"
    },
    "casual": {
        "template": "Formuliere einen lockeren, verständlichen Prompt über: {topic}",
        "description": "Umgangssprachlich, zugänglich"
    }
}


def apply_style(topic: str, style: str = "technisch") -> str:
    """
    Wendet einen Prompt-Style auf ein Topic an.
    
    Args:
        topic: Das Thema
        style: Der Style (technisch, kreativ, akademisch, casual)
        
    Returns:
        Formatierter Prompt
    """
    if style not in PROMPT_STYLES:
        style = "technisch"  # Fallback
    
    template = PROMPT_STYLES[style]["template"]
    return template.format(topic=topic)


def get_all_styles() -> list:
    """Gibt alle verfügbaren Styles zurück."""
    return list(PROMPT_STYLES.keys())


def get_style_info(style: str) -> dict:
    """Gibt Infos zu einem Style zurück."""
    return PROMPT_STYLES.get(style, PROMPT_STYLES["technisch"])


if __name__ == "__main__":
    # Test
    topic = "Künstliche Intelligenz"
    
    print(f"Topic: {topic}\n")
    print("="*60)
    
    for style in get_all_styles():
        prompt = apply_style(topic, style)
        info = get_style_info(style)
        print(f"\n{style.upper()}:")
        print(f"  {info['description']}")
        print(f"  → {prompt}")
    
    print("\n" + "="*60)
