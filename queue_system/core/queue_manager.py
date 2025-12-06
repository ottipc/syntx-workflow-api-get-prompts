"""
Queue Manager - Zentraler Orchestrator

=== ZWECK ===
Entscheidet ob und wie viel produziert werden soll
Basierend auf Queue-Zustand und Processing Rate

=== HAUPTAUFGABE ===
should_produce() → (bool, int)
- bool: Soll produziert werden?
- int: Wie viele Prompts?

=== DECISION LOGIC ===
State-basiert:
- STARVING → Produziere MAX (20)
- LOW → Produziere MEDIUM (15)
- BALANCED → Produziere MIN (10)
- HIGH → Produziere nichts
- OVERFLOW → Produziere nichts + Alert
"""
from datetime import datetime, timedelta
from typing import Tuple, Dict, Any

# Imports
from ..monitoring.queue_monitor import QueueMonitor
from ..config.queue_config import *


class QueueManager:
    """
    Zentraler Orchestrator für Queue-System
    
    === RESPONSIBILITIES ===
    1. Queue-Zustand überwachen
    2. Producer-Aktivierung entscheiden
    3. System-Health bewerten
    4. Status-Reports generieren
    
    === KEINE RESPONSIBILITIES ===
    - Keine File-Operations (das macht FileHandler)
    - Keine Kalibrierung (das macht Consumer)
    - Kein Logging (das macht jedes Modul selbst)
    
    === DESIGN PATTERN ===
    Facade Pattern - vereinfacht Zugriff auf komplexes System
    """
    
    def __init__(self):
        """
        Initialisiert Manager mit Monitor
        
        Monitor ist stateless - kann jederzeit neu erstellt werden
        """
        self.monitor = QueueMonitor()
    
    def should_produce(self) -> Tuple[bool, int]:
        """
        Entscheidet ob produziert werden soll
        
        === DECISION TREE ===
        1. Hole Queue-Status vom Monitor
        2. Bestimme State (STARVING/LOW/BALANCED/HIGH/OVERFLOW)
        3. Entscheide Menge basierend auf State
        
        === LOGIC ===
        STARVING (0 Jobs):
            → CRITICAL! Produziere MAX (20)
            → System hat KEINE Arbeit
        
        LOW (1-4 Jobs):
            → Produziere MEDIUM (15)
            → System braucht bald Nachschub
        
        BALANCED (5-24 Jobs):
            → Produziere MIN (10)
            → Sanft nachfüllen
        
        HIGH (25-49 Jobs):
            → Produziere NICHTS
            → Genug Arbeit vorhanden
        
        OVERFLOW (50+ Jobs):
            → Produziere NICHTS
            → Consumer kommt nicht hinterher
            → Monitoring sollte Alert senden
        
        === RETURNS ===
        (should_produce, how_many)
        - should_produce: bool - Soll GPT aktiviert werden?
        - how_many: int - Wie viele Prompts generieren?
        
        === BEISPIELE ===
        Queue leer → (True, 20)
        Queue hat 3 → (True, 15)
        Queue hat 12 → (True, 10)
        Queue hat 30 → (False, 0)
        Queue hat 100 → (False, 0)
        """
        # Status vom Monitor holen
        status = self.monitor.get_status()
        queue_count = status['queue']['incoming']
        state = status['state']
        
        # Decision basierend auf State
        if state == "STARVING":
            # CRITICAL: Keine Arbeit
            # Produziere Maximum sofort
            return True, PRODUCER_BATCH_SIZE
        
        elif state == "LOW":
            # Bald leer
            # Produziere Medium
            return True, int(PRODUCER_BATCH_SIZE * 0.75)  # 15 bei BATCH_SIZE=20
        
        elif state == "BALANCED":
            # Optimal
            # Sanft nachfüllen
            return True, int(PRODUCER_BATCH_SIZE * 0.5)  # 10 bei BATCH_SIZE=20
        
        elif state == "HIGH":
            # Viel Arbeit
            # Keine Produktion nötig
            return False, 0
        
        else:  # OVERFLOW
            # Zu viel Arbeit
            # Keine Produktion + Alert
            return False, 0
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Vollständiger System-Status für Monitoring
        
        === VERWENDUNG ===
        - Dashboards
        - CLI Status-Tool
        - Logging
        - Alerts
        
        === OUTPUT ===
        {
            "timestamp": "...",
            "queue": {
                "incoming": 12,
                "processing": 2,
                "processed": 450,
                "error": 3
            },
            "state": "BALANCED",
            "producer": {
                "should_run": true,
                "batch_size": 10
            },
            "health": "OK"
        }
        
        === RETURNS ===
        dict: Vollständiger Status-Report
        """
        # Queue Status vom Monitor
        status = self.monitor.get_status()
        
        # Producer Decision
        should_run, batch_size = self.should_produce()
        
        # Health Check
        health = self._determine_health(status)
        
        # Kombinierter Status
        return {
            "timestamp": status['timestamp'],
            "queue": status['queue'],
            "state": status['state'],
            "producer": {
                "should_run": should_run,
                "batch_size": batch_size
            },
            "health": health
        }
    
    def _determine_health(self, status: Dict) -> str:
        """
        Bestimmt System-Health
        
        === HEALTH STATES ===
        OK: Alles normal
        WARNING: Overflow oder viele Errors
        CRITICAL: Processing stalled oder extreme Overflow
        
        === CHECKS ===
        1. Processing > 0 aber < 5 für >1h → Worker crashed?
        2. Error > 10 → Viele Fehler
        3. Overflow → Consumer zu langsam
        
        === ARGS ===
        status: Status-Dict vom Monitor
        
        === RETURNS ===
        str: "OK" | "WARNING" | "CRITICAL"
        """
        state = status['state']
        error_count = status['queue']['error']
        
        # Critical Checks
        if state == "OVERFLOW":
            return "CRITICAL"  # Zu viele Jobs
        
        # Warning Checks
        if error_count > 10:
            return "WARNING"  # Viele Fehler
        
        if state == "HIGH":
            return "WARNING"  # Viel Arbeit
        
        # Sonst OK
        return "OK"


# === MAIN BLOCK ===
if __name__ == "__main__":
    import json
    
    # Manager erstellen
    manager = QueueManager()
    
    # System Status holen
    status = manager.get_system_status()
    
    # Pretty Print
    print("=== QUEUE MANAGER STATUS ===")
    print(json.dumps(status, indent=2))
    
    # Decision explizit zeigen
    should_run, batch_size = manager.should_produce()
    print(f"\n=== PRODUCER DECISION ===")
    print(f"Should Run: {should_run}")
    print(f"Batch Size: {batch_size}")
