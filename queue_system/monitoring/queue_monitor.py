"""
Queue Monitoring - Real-Time Queue Status

=== ZWECK ===
Dieses Modul überwacht den Zustand des Queue-Systems in Echtzeit.
Es zählt Jobs in allen Queue-Ordnern und bestimmt den System-Zustand.

=== ARCHITEKTUR ===
- Keine State-Speicherung (stateless)
- Jeder Aufruf liest direkt vom Filesystem
- Pure Functions - nur Zählen und Analysieren
- Kein Locking nötig (nur lesend)

=== VERWENDUNG ===
    monitor = QueueMonitor()
    status = monitor.get_status()
    # → {"queue": {"incoming": 12, ...}, "state": "BALANCED"}
"""
from pathlib import Path
import json
from datetime import datetime

# Config importieren (Pfade + Thresholds)
from ..config.queue_config import *


class QueueMonitor:
    """
    Überwacht Queue-Zustand in Echtzeit
    
    === DESIGN PATTERN ===
    Observer Pattern - beobachtet Filesystem ohne zu modifizieren
    
    === THREAD-SAFETY ===
    Thread-safe weil read-only operations
    Mehrere Monitor-Instanzen können parallel laufen
    
    === PERFORMANCE ===
    O(n) pro count Operation wo n = Anzahl Dateien im Ordner
    Bei 1000 Dateien: ~1-2ms pro Operation
    """
    
    def count_incoming(self) -> int:
        """
        Zählt wartende Jobs in incoming/
        
        === WAS WIRD GEZÄHLT ===
        Alle .txt Dateien in queue/incoming/
        Jede .txt Datei = 1 Job der verarbeitet werden muss
        
        === WARUM NUR .txt ===
        Metadata liegt in .json Dateien
        Nur .txt Dateien sind die eigentlichen Jobs
        
        === RETURNS ===
        int: Anzahl wartender Jobs (0 = Queue leer)
        
        === BEISPIEL ===
        queue/incoming/
        ├── 20251127_120000__topic_AI__style_technisch.txt
        ├── 20251127_120001__topic_Klima__style_kreativ.txt
        └── 20251127_120002__topic_Physik__style_casual.txt
        
        → count = 3
        """
        # glob("*.txt") findet alle .txt Dateien
        # list() konvertiert Generator zu Liste
        # len() zählt Liste
        return len(list(QUEUE_INCOMING.glob("*.txt")))
    
    def count_processing(self) -> int:
        """
        Zählt Jobs die gerade verarbeitet werden
        
        === BEDEUTUNG ===
        Jobs in processing/ = von einem Worker gelocked
        Worker hat Datei von incoming/ nach processing/ verschoben (atomic)
        
        === LOCK PATTERN ===
        File-Based Locking:
        1. Worker versucht: incoming/job.txt → processing/job.txt
        2. Wenn erfolgreich: Worker hat den Lock
        3. Wenn FileNotFoundError: Anderer Worker war schneller
        
        === WARNUNG ===
        Wenn count > 0 für lange Zeit (>1h):
        → Worker ist abgestürzt
        → Datei manuell zurück nach incoming/ verschieben
        
        === RETURNS ===
        int: Anzahl Jobs in Bearbeitung
        """
        # Gleiche Logik wie count_incoming
        # Aber anderer Ordner
        return len(list(QUEUE_PROCESSING.glob("*.txt")))
    
    def count_processed(self) -> int:
        """
        Zählt erfolgreich verarbeitete Jobs
        
        === BEDEUTUNG ===
        Jobs in processed/ = erfolgreich durch SYNTX gelaufen
        Diese Jobs haben:
        - Meta-Prompt erhalten
        - SYNTX Wrapper bekommen
        - Llama Kalibrierung durchlaufen
        - Quality Score >= Threshold
        
        === ARCHIVIERUNG ===
        Diese Dateien werden nach X Tagen nach archive/ verschoben
        (siehe ARCHIVE_AFTER_DAYS in config)
        
        === MONITORING ===
        Wachstum dieser Zahl = System-Produktivität
        
        === RETURNS ===
        int: Anzahl erfolgreicher Jobs (lifetime seit letztem cleanup)
        """
        return len(list(QUEUE_PROCESSED.glob("*.txt")))
    
    def count_error(self) -> int:
        """
        Zählt fehlgeschlagene Jobs
        
        === BEDEUTUNG ===
        Jobs in error/ = Processing fehlgeschlagen
        Gründe können sein:
        - Llama Timeout (504)
        - Llama Connection Error
        - Parse Error (Response nicht SYNTX-konform)
        - Quality Score zu niedrig
        
        === RETRY PATTERN ===
        Jobs in error/ haben Retry-Count im Filename:
        - job__retry1.txt (1. Fehler)
        - job__retry2.txt (2. Fehler)
        - job__retry3.txt (3. Fehler - dann aufgeben)
        
        === MANUAL RETRY ===
        Admin kann Job manuell zurück nach incoming/ verschieben
        
        === RETURNS ===
        int: Anzahl fehlgeschlagener Jobs
        """
        return len(list(QUEUE_ERROR.glob("*.txt")))
    
    def get_status(self) -> dict:
        """
        Liefert vollständigen Queue-Status Snapshot
        
        === VERWENDUNG ===
        Für:
        - Monitoring Dashboards
        - Alert Systems
        - Producer Decision Logic
        - Admin CLI Tools
        
        === OUTPUT STRUKTUR ===
        {
            "timestamp": "2025-11-27T12:00:00.123456",
            "queue": {
                "incoming": 12,    # Wartend
                "processing": 2,   # In Arbeit
                "processed": 450,  # Erfolgreich
                "error": 3         # Failed
            },
            "state": "BALANCED"    # System-Zustand
        }
        
        === SYSTEM STATES ===
        - STARVING: Keine Arbeit (incoming = 0)
        - LOW: Bald leer (incoming < 5)
        - BALANCED: Optimal (incoming 5-25)
        - HIGH: Viel Arbeit (incoming 25-50)
        - OVERFLOW: Zu viel (incoming > 50)
        
        === RETURNS ===
        dict: Status-Snapshot mit allen Metriken
        """
        # Incoming Count holen für State-Bestimmung
        # Dieser Wert ist der wichtigste für Producer-Entscheidung
        incoming = self.count_incoming()
        
        # Status-Dict bauen
        return {
            # ISO Timestamp für Log-Parsing
            "timestamp": datetime.now().isoformat(),
            
            # Queue Counts - alle Ordner
            "queue": {
                "incoming": incoming,           # Wie viel Arbeit wartet
                "processing": self.count_processing(),  # Wie viel läuft gerade
                "processed": self.count_processed(),    # Wie viel erfolgreich
                "error": self.count_error()             # Wie viel fehlgeschlagen
            },
            
            # System-Zustand basierend auf incoming count
            # Producer nutzt diesen Wert für Entscheidung
            "state": self._determine_state(incoming)
        }
    
    def _determine_state(self, count: int) -> str:
        """
        Bestimmt System-Zustand basierend auf incoming count
        
        === DECISION LOGIC ===
        Diese Funktion ist das HERZ der Producer-Steuerung
        
        Thresholds (aus config):
        - QUEUE_MIN_THRESHOLD = 5
        - QUEUE_MAX_THRESHOLD = 50
        
        Decision Tree:
        1. count == 0        → STARVING (Producer MUSS aktivieren)
        2. count < 5         → LOW (Producer sollte bald aktivieren)
        3. count < 25 (50/2) → BALANCED (optimal, sanft nachfüllen)
        4. count < 50        → HIGH (viel Arbeit, Producer pausiert)
        5. count >= 50       → OVERFLOW (zu viel, Consumer zu langsam, ALARM)
        
        === PRODUCER REAKTION ===
        - STARVING → Produziere 20 Prompts sofort
        - LOW → Produziere 15 Prompts
        - BALANCED → Produziere 10 Prompts (sanft nachfüllen)
        - HIGH → Produziere nichts
        - OVERFLOW → Produziere nichts + Alert
        
        === ARGS ===
        count: Anzahl Jobs in incoming/
        
        === RETURNS ===
        str: State-String für Monitoring/Logging
        """
        # Case 1: Queue komplett leer
        # → System hat KEINE Arbeit
        # → Producer muss sofort aktivieren
        if count == 0:
            return "STARVING"
        
        # Case 2: Unter Minimum-Threshold
        # → Queue wird bald leer sein
        # → Producer sollte bald aktivieren
        elif count < QUEUE_MIN_THRESHOLD:
            return "LOW"
        
        # Case 3: Zwischen Min und 50% von Max
        # → Optimal-Zustand
        # → Genug Arbeit aber nicht zu viel
        # → Producer kann sanft nachfüllen
        elif count < QUEUE_MAX_THRESHOLD // 2:
            return "BALANCED"
        
        # Case 4: Zwischen 50% und Max
        # → Viel Arbeit vorhanden
        # → Consumer arbeitet
        # → Producer kann pausieren
        elif count < QUEUE_MAX_THRESHOLD:
            return "HIGH"
        
        # Case 5: Über Maximum
        # → Zu viel Arbeit
        # → Consumer kommt nicht hinterher
        # → Producer MUSS pausieren
        # → Monitoring sollte Alert senden
        else:
            return "OVERFLOW"


# === MAIN BLOCK ===
# Wird ausgeführt wenn Datei direkt gestartet: python3 queue_monitor.py
# Nicht ausgeführt wenn importiert: from queue_monitor import QueueMonitor
if __name__ == "__main__":
    # Quick Test - zeigt aktuellen Queue-Status im Terminal
    
    # Monitor-Instanz erstellen
    monitor = QueueMonitor()
    
    # Status holen (liest vom Filesystem)
    status = monitor.get_status()
    
    # Pretty-Print als JSON
    # indent=2 macht es lesbar
    print(json.dumps(status, indent=2))
