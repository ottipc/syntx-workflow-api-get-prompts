"""
Prompt Styles - Config-Driven
Lädt Styles aus /opt/syntx-config/configs/generator.yaml
"""
import random
import sys
from pathlib import Path
from typing import List

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config_loader import get_config


def get_all_styles() -> List[str]:
    """
    Holt alle verfügbaren Styles aus Config.
    
    Returns:
        List of style names
    """
    return get_config('generator', 'styles', 'available', default=[])


def get_default_style() -> str:
    """
    Holt den Default Style.
    
    Returns:
        Default style name
    """
    return get_config('generator', 'styles', 'default', default='technisch')


def get_random_style() -> str:
    """
    Wählt einen zufälligen Style.
    
    Returns:
        Random style name
    """
    styles = get_all_styles()
    return random.choice(styles) if styles else 'technisch'


def apply_style(prompt: str, style: str) -> str:
    """
    Wendet einen Style auf einen Prompt an.
    
    Args:
        prompt: Original prompt
        style: Style name
        
    Returns:
        Styled prompt
    """
    # Style-spezifische Präfixe
    style_prefixes = {
        'technisch': 'Erkläre technisch und präzise: ',
        'kreativ': 'Erkläre kreativ und metaphorisch: ',
        'akademisch': 'Erkläre in wissenschaftlichem Stil: ',
        'casual': 'Erkläre in lockerer, verständlicher Sprache: '
    }
    
    prefix = style_prefixes.get(style, '')
    return f"{prefix}{prompt}" if prefix else prompt


if __name__ == "__main__":
    # Test
    print("🎨 Prompt Styles (Config-Driven)\n")
    
    styles = get_all_styles()
    print(f"Available Styles: {styles}")
    print(f"Default Style: {get_default_style()}")
    print(f"Random Style: {get_random_style()}\n")
    
    # Test apply_style
    test_prompt = "Was ist Quantencomputer?"
    for style in styles:
        styled = apply_style(test_prompt, style)
        print(f"[{style}]")
        print(f"  {styled}\n")
