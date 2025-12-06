"""
Intelligent Producer - Queue-Aware GPT Prompt Generator

=== ZWECK ===
Produziert Prompts NUR wenn Queue sie braucht
Nutzt QueueManager für Entscheidung
Nutzt FileHandler für Atomic Writes

=== FLOW ===
1. Check: Soll produziert werden? (QueueManager)
2. Ja → Wähle Topics aus
3. Generiere via GPT
4. Schreibe in Queue (FileHandler)
5. Log Production Event

=== KEIN BLIND PRODUCING ===
Nicht: "Generiere immer 20"
Sondern: "Frag Queue ob nötig, dann wie viel"
"""
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

# Add parent to path für GPT Generator Import
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gpt_generator.syntx_prompt_generator import generate_prompt
from gpt_generator.topics_database import get_random_topics

from .queue_manager import QueueManager
from .file_handler import FileHandler


class IntelligentProducer:
    """
    Queue-Aware Producer
    
    === DESIGN ===
    Self-Regulating - prüft Queue bevor Produktion
    
    === DEPENDENCIES ===
    - QueueManager: Für Decision Logic
    - FileHandler: Für Atomic Writes
    - GPT Generator: Für Prompt Creation
    - Topics Database: Für Topic Selection
    """
    
    def __init__(self):
        """
        Initialisiert Producer mit Dependencies
        """
        self.queue_manager = QueueManager()
        self.file_handler = FileHandler()
    
    def run(self, force: bool = False) -> dict:
        """
        Haupt-Logik: Check & Produce
        
        === FLOW ===
        1. Hole Decision vom QueueManager
        2. Wenn nicht produzieren → Skip & Log
        3. Wenn produzieren → Generate & Write
        4. Return Stats
        
        === FORCE MODE ===
        force=True → Ignoriert Queue-Zustand, produziert immer
        Nur für Testing/Manual Runs
        
        === ARGS ===
        force: bool - Ignoriere Queue-Check?
        
        === RETURNS ===
        dict mit:
        - should_produce: bool
        - requested_count: int
        - produced_count: int
        - skipped: bool
        - duration_seconds: float
        """
        start_time = datetime.now()
        
        # === DECISION PHASE ===
        if not force:
            should_produce, count = self.queue_manager.should_produce()
            
            if not should_produce:
                # Queue hat genug - Skip
                return {
                    "should_produce": False,
                    "requested_count": 0,
                    "produced_count": 0,
                    "skipped": True,
                    "reason": "Queue sufficient",
                    "duration_seconds": 0
                }
        else:
            # Force Mode - produziere default amount
            count = 20
            should_produce = True
        
        print(f"🔧 Producer aktiviert - Generiere {count} Prompts...")
        
        # === PRODUCTION PHASE ===
        # Topics wählen
        topics = get_random_topics(count)
        
        success_count = 0
        failed_count = 0
        
        # Für jeden Topic: GPT → Queue
        for i, (category, topic) in enumerate(topics, 1):
            print(f"[{i}/{count}] {category}: {topic}")
            
            # Style random wählen (wie in batch_generator)
            import random
            style = random.choice(['technisch', 'kreativ', 'akademisch', 'casual'])
            
            # GPT generieren
            result = generate_prompt(
                prompt=topic,
                style=style,
                category=category,
                max_tokens=400,
                max_refusal_retries=3
            )
            
            if result['success']:
                # In Queue schreiben (atomic)
                meta_prompt = result['prompt_generated']
                
                metadata = {
                    "topic": topic,
                    "style": style,
                    "category": category,
                    "gpt_quality": result['quality_score'],
                    "gpt_cost": result['cost'],
                    "producer_run": datetime.now().isoformat()
                }
                
                try:
                    # Atomic write to queue
                    from ..config.queue_config import QUEUE_INCOMING
                    self.file_handler.atomic_write(
                        content=meta_prompt,
                        metadata=metadata,
                        target_dir=QUEUE_INCOMING
                    )
                    success_count += 1
                    print(f"   ✅ In Queue geschrieben")
                except Exception as e:
                    print(f"   ❌ Queue Write Failed: {e}")
                    failed_count += 1
            else:
                print(f"   ❌ GPT Failed: {result.get('error')}")
                failed_count += 1
        
        # === STATS ===
        duration = (datetime.now() - start_time).total_seconds()
        
        stats = {
            "should_produce": should_produce,
            "requested_count": count,
            "produced_count": success_count,
            "failed_count": failed_count,
            "skipped": False,
            "duration_seconds": duration
        }
        
        print(f"\n✅ Production Complete:")
        print(f"   Success: {success_count}/{count}")
        print(f"   Failed: {failed_count}")
        print(f"   Duration: {duration:.1f}s")
        
        return stats


# === MAIN BLOCK ===
if __name__ == "__main__":
    import json
    
    print("=== INTELLIGENT PRODUCER TEST ===\n")
    
    # Producer erstellen
    producer = IntelligentProducer()
    
    # Run (checkt Queue automatisch)
    stats = producer.run()
    
    print(f"\n=== STATS ===")
    print(json.dumps(stats, indent=2))
