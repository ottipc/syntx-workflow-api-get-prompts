"""
SYNTEX Wrapper Loader
"""

from pathlib import Path
from typing import Optional

from ..utils.exceptions import WrapperNotFoundError


# Wrapper Storage (Projekt-Root/wrappers)
WRAPPER_DIR = Path(__file__).parent.parent.parent.parent / "wrappers"

AVAILABLE_WRAPPERS = {
    "human": WRAPPER_DIR / "syntex_wrapper_human.txt",
    "sigma": WRAPPER_DIR / "syntex_wrapper_sigma.txt",
    "sigma_v2": WRAPPER_DIR / "syntex_wrapper_sigma_v2.txt"
}


class SyntexWrapper:
    def __init__(self, wrapper_name: str = "human"):
        """
        Args:
            wrapper_name: Name ('human', 'sigma', 'sigma_v2') oder Path zu custom Wrapper
        """
        if wrapper_name in AVAILABLE_WRAPPERS:
            self.wrapper_file = AVAILABLE_WRAPPERS[wrapper_name]
        else:
            # Custom path
            self.wrapper_file = Path(wrapper_name)
        
        self.template = None
    
    def load(self) -> str:
        """Lädt Wrapper-Template"""
        # Prüfe ob Path existiert
        if not self.wrapper_file.exists():
            available = ", ".join(AVAILABLE_WRAPPERS.keys())
            raise WrapperNotFoundError(
                f"Wrapper nicht gefunden: {self.wrapper_file}\n"
                f"Verfügbare: {available}"
            )
        
        with open(self.wrapper_file, 'r', encoding='utf-8') as f:
            self.template = f.read()
        
        return self.template
    
    def build_prompt(self, meta_prompt: str) -> str:
        """Baut finalen Prompt"""
        if not self.template:
            self.load()
        
        return self.template + "\n" + meta_prompt
    
    @staticmethod
    def list_available():
        """Liste verfügbare Wrapper"""
        return list(AVAILABLE_WRAPPERS.keys())
