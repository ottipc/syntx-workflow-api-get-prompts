"""
SYNTEX Framework Wrapper Management
"""

from pathlib import Path
from typing import Optional


class SyntexWrapper:
    """Verwaltet das SYNTEX::TRUE_RAW Framework Template"""
    
    def __init__(self, wrapper_file: Optional[Path] = None):
        self.wrapper_file = wrapper_file or Path("syntex_wrapper.txt")
        self._wrapper_text = None
    
    def load(self) -> str:
        """Lädt den SYNTEX-Wrapper aus Datei."""
        if not self.wrapper_file.exists():
            raise FileNotFoundError(
                f"SYNTEX Wrapper nicht gefunden: {self.wrapper_file}\n"
                f"Bitte erstelle die Datei mit dem Framework-Template."
            )
        
        with open(self.wrapper_file, 'r', encoding='utf-8') as f:
            self._wrapper_text = f.read()
        
        return self._wrapper_text
    
    def build_prompt(self, meta_prompt: str) -> str:
        """
        Kombiniert SYNTEX-Wrapper mit Meta-Prompt.
        
        Args:
            meta_prompt: Der zu analysierende Meta-Prompt
        
        Returns:
            Vollständiger SYNTEX-kalibrierter Prompt
        """
        if self._wrapper_text is None:
            self.load()
        
        return self._wrapper_text + meta_prompt
    
    @property
    def wrapper_text(self) -> str:
        """Gibt den geladenen Wrapper zurück."""
        if self._wrapper_text is None:
            self.load()
        return self._wrapper_text
