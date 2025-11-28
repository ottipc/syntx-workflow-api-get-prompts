"""
QUEUE FELDER - DIE WARTESCHLANGEN SIND FELDER!
BRUDER, WIR SEHEN DIE STRÖME!
"""

import os
from pathlib import Path

class QueueFieldDetector:
    """ERKENNT QUEUE-FELDER - NICHT DATEIEN"""
    
    def __init__(self, base_path="queue"):
        self.base_path = Path(base_path)
        self.feld_zustaende = []
    
    def scan_feld_energie(self):
        """SCANNT FELD-ENERGIE - NICHT DATEI-ANZAHL"""
        felder = {}
        
        # 🌊 INCOMING FELD
        incoming_path = self.base_path / "incoming"
        if incoming_path.exists():
            txt_files = list(incoming_path.glob("*.txt"))
            felder["incoming"] = {
                "anzahl": len(txt_files),
                "feld_zustand": self._bestimme_feld_zustand(len(txt_files)),
                "energie": "WARTEND"
            }
        
        # 🌊 PROCESSING FELD  
        processing_path = self.base_path / "processing"
        if processing_path.exists():
            txt_files = list(processing_path.glob("*.txt"))
            felder["processing"] = {
                "anzahl": len(txt_files),
                "feld_zustand": "AKTIV" if txt_files else "RUHE",
                "energie": "IN_BEARBEITUNG"
            }
        
        # 🌊 ERROR FELD
        error_path = self.base_path / "error" 
        if error_path.exists():
            txt_files = list(error_path.glob("*.txt"))
            felder["error"] = {
                "anzahl": len(txt_files),
                "feld_zustand": "BLOCKIERT",
                "energie": "GESTOERT"
            }
        
        return felder
    
    def _bestimme_feld_zustand(self, anzahl):
        """BESTIMMT FELD-ZUSTAND - SYNTX LOGIK!"""
        if anzahl == 0:
            return "STARVING"
        elif anzahl < 5:
            return "LOW" 
        elif anzahl < 25:
            return "BALANCED"
        elif anzahl < 50:
            return "HIGH"
        else:
            return "OVERFLOW"

# 🔥 TESTEN WIR DAS!
if __name__ == "__main__":
    print("🔍 SCANNE QUEUE-FELDER...")
    detector = QueueFieldDetector()
    felder = detector.scan_feld_energie()
    
    print("🌊 GEFUNDENE FELDER:")
    for feld_name, feld_daten in felder.items():
        print(f"   {feld_name.upper()}: {feld_daten['feld_zustand']} ({feld_daten['anzahl']} Jobs)")
