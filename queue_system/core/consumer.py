"""
Queue Consumer - SYNTX Worker mit File-Based Locking

=== ZWECK ===
Verarbeitet Jobs aus Queue durch SYNTX-Kalibrierung
Nutzt Atomic Move für Lock-Pattern (keine Race Conditions)

=== FLOW ===
1. Hole ältesten Job aus incoming/ (atomic move → processing/)
2. Lade Meta-Prompt + Metadata
3. SYNTX Wrapper anwenden
4. Llama kalibrieren
5. Parse + Score Response
6. Move zu processed/ (success) oder error/ (failed)

=== LOCK PATTERN ===
File-Based Locking via Atomic Rename:
- incoming/job.txt → processing/job.txt = Lock acquired
- Wenn rename fails → Job bereits von anderem Worker gelocked
- Ermöglicht parallele Worker ohne Koordination
"""
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple
from dataclasses import dataclass

# Add parent for SYNTX imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from syntex_injector.syntex.core.calibrator_enhanced import EnhancedSyntexCalibrator

# WRAPPER PATCHER - Dynamic Loading from /opt/syntx-config/wrappers/
from queue_system.utils.wrapper_patcher import patch_wrapper_system
patched_wrappers = patch_wrapper_system()

from .file_handler import FileHandler
from ..config.queue_config import *


@dataclass
class Job:
    """
    Job Container
    
    === FIELDS ===
    - file_path: Path zum .txt File in processing/
    - meta_path: Path zum .json File
    - content: Meta-Prompt Text
    - metadata: Job Metadata (topic, style, gpt_quality, etc.)
    - filename: Original Filename
    """
    file_path: Path
    meta_path: Path
    content: str
    metadata: dict
    filename: str


class QueueConsumer:
    """
    SYNTX Queue Worker
    
    === DESIGN ===
    Stateless Worker - kann parallel laufen
    Jeder Worker konkurriert um Jobs via File-Lock
    
    === GUARANTEES ===
    - Kein Job wird doppelt verarbeitet (atomic lock)
    - Kein Job geht verloren (atomic moves)
    - Fehler werden geloggt + retry-count erhöht
    """
    
    def __init__(self, wrapper_name: str = "human", worker_id: Optional[str] = None):
        """
        Initialisiert Consumer
        
        === ARGS ===
        wrapper_name: "human" | "sigma" | "sigma_v2"
        worker_id: Optional ID für Logging (default: PID)
        """
        import os
        self.worker_id = worker_id or f"worker_{os.getpid()}"
        self.wrapper_name = wrapper_name
        
        # SYNTX Calibrator
        self.calibrator = EnhancedSyntexCalibrator(wrapper_name=wrapper_name)
        
        # File Handler
        self.file_handler = FileHandler()
        
        print(f"🔧 Consumer [{self.worker_id}] initialized (wrapper: {wrapper_name})")
    
    def get_next_job(self) -> Optional[Job]:
        """
        Holt nächsten Job aus Queue MIT LOCK
        
        === LOCK MECHANISM ===
        1. Liste alle .txt Files in incoming/ (sortiert nach Timestamp)
        2. Versuche älteste Datei: incoming/ → processing/
        3. Wenn rename() erfolgreich → Lock acquired, return Job
        4. Wenn FileNotFoundError → anderer Worker war schneller, try next
        5. Wenn keine Files mehr → return None (Queue leer)
        
        === WARUM ATOMIC ===
        rename() ist atomic auf POSIX filesystems
        Entweder: File ist verschoben (Lock acquired)
        Oder: FileNotFoundError (Lock von anderem Worker)
        Niemals: Partial state oder doppeltes Processing
        
        === RETURNS ===
        Job object wenn erfolgreich gelocked
        None wenn Queue leer
        """
        # Alle .txt Files in incoming/ (sortiert = älteste zuerst)
        # Get all .txt files EXCEPT _response.txt files!
        all_txt_files = sorted(QUEUE_INCOMING.glob("*.txt"))
        incoming_files = [f for f in all_txt_files if not f.name.endswith('_response.txt')]
        
        if not incoming_files:
            return None  # Queue leer
        
        # Versuche jedes File zu locken (älteste zuerst)
        for file_path in incoming_files:
            try:
                # === ATOMIC LOCK ===
                # Target in processing/
                processing_path = QUEUE_PROCESSING / file_path.name
                
                # Atomic rename = Lock
                # Wenn das wirft FileNotFoundError → anderer Worker hat's
                file_path.rename(processing_path)
                
                # === LOCK ACQUIRED! ===
                # Metadata auch verschieben
                meta_path_incoming = file_path.with_suffix('.json')
                meta_path_processing = processing_path.with_suffix('.json')
                
                if meta_path_incoming.exists():
                    meta_path_incoming.rename(meta_path_processing)
                
                # Job laden
                return self._load_job(processing_path, meta_path_processing)
                
            except FileNotFoundError:
                # Anderer Worker war schneller
                # Try next file
                continue
            except Exception as e:
                print(f"⚠️  Error locking {file_path.name}: {e}")
                continue
        
        # Alle Files waren bereits gelocked
        return None
    
    def _load_job(self, file_path: Path, meta_path: Path) -> Job:
        """
        Lädt Job-Content + Metadata
        
        === ARGS ===
        file_path: Path zum .txt in processing/
        meta_path: Path zum .json in processing/
        
        === RETURNS ===
        Job object mit allen Daten
        """
        # Content laden
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Metadata laden
        import json
        if meta_path.exists():
            with open(meta_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        else:
            metadata = {}
        
        return Job(
            file_path=file_path,
            meta_path=meta_path,
            content=content,
            metadata=metadata,
            filename=file_path.name
        )
    
    def process_job(self, job: Job) -> bool:
        """
        Verarbeitet einen Job durch SYNTX Pipeline
        
        === FLOW ===
        1. SYNTX Kalibrierung (Wrapper + Llama + Parse + Score)
        2. Wenn Success → move to processed/
        3. Wenn Failed → move to error/ (mit retry-count)
        
        === ARGS ===
        job: Job object aus get_next_job()
        
        === RETURNS ===
        bool: Success status
        """
        print(f"\n{'='*60}")
        print(f"Processing: {job.filename}")
        print(f"Topic: {job.metadata.get('topic', 'unknown')}")
        print(f"Style: {job.metadata.get('style', 'unknown')}")
        print(f"{'='*60}")
        
        try:
            # === SYNTX KALIBRIERUNG ===
            success, response, result_meta = self.calibrator.calibrate(
                meta_prompt=job.content,
                verbose=True,  # Zeigt Llama Output
                show_quality=True  # Zeigt Quality Score
            )
            
            if success:
                # === SUCCESS PATH ===
                print(f"✅ Kalibrierung erfolgreich!")
                
                # Metadata updaten
                job.metadata['syntex_result'] = {
                    'quality_score': result_meta.get('quality_score'),
                    'duration_ms': result_meta.get('duration_ms'),
                    'session_id': result_meta.get('session_id'),
                    'wrapper': self.wrapper_name,
                    'worker_id': self.worker_id,
                    'response_text': response  # ← RESPONSE SPEICHERN!
                }
                
                # Move zu processed/ FIRST!
                self.file_handler.move_to_processed(job)
                
                # THEN save response in processed/ (not processing/!)
                if response:
                    # Use QUEUE_PROCESSED - file is now in processed/!
                    response_file = QUEUE_PROCESSED / (job.filename.replace('.txt', '_response.txt'))
                    with open(response_file, 'w', encoding='utf-8') as f:
                        f.write(response)
                    print(f"  💾 Response saved to: {response_file}")
                
                return True
                
            else:
                # === FAILURE PATH ===
                error_info = {
                    'error': result_meta.get('error', 'Unknown error'),
                    'duration_ms': result_meta.get('duration_ms'),
                    'worker_id': self.worker_id,
                    'wrapper': self.wrapper_name
                }
                
                print(f"❌ Kalibrierung fehlgeschlagen: {error_info['error']}")
                
                # Move zu error/ (mit retry-count)
                self.file_handler.move_to_error(job, error_info)
                
                return False
                
        except Exception as e:
            # === EXCEPTION PATH ===
            print(f"❌ Exception während Processing: {e}")
            
            error_info = {
                'error': str(e),
                'exception_type': type(e).__name__,
                'worker_id': self.worker_id
            }
            
            # Move zu error/
            self.file_handler.move_to_error(job, error_info)
            
            return False
    
    def process_batch(self, batch_size: int = 20) -> dict:
        """
        Verarbeitet Batch von Jobs
        
        === FLOW ===
        Loop bis:
        - batch_size erreicht ODER
        - Queue leer
        
        === ARGS ===
        batch_size: Max Anzahl Jobs zu verarbeiten
        
        === RETURNS ===
        dict mit Stats:
        - processed: Anzahl erfolgreicher Jobs
        - failed: Anzahl fehlgeschlagener Jobs
        - total: Gesamt
        - duration_seconds: Gesamt-Dauer
        """
        start_time = datetime.now()
        
        stats = {
            'processed': 0,
            'failed': 0,
            'total': 0
        }
        
        print(f"\n🚀 Starting batch processing (max: {batch_size} jobs)")
        print(f"Worker: {self.worker_id}")
        print(f"Wrapper: {self.wrapper_name}\n")
        
        for i in range(batch_size):
            # Nächsten Job holen (mit Lock)
            job = self.get_next_job()
            
            if not job:
                print(f"\n📭 Queue empty after {stats['total']} jobs")
                break
            
            # Job verarbeiten
            success = self.process_job(job)
            
            stats['total'] += 1
            if success:
                stats['processed'] += 1
            else:
                stats['failed'] += 1
        
        # Duration
        duration = (datetime.now() - start_time).total_seconds()
        stats['duration_seconds'] = duration
        
        # Summary
        print(f"\n{'='*60}")
        print(f"BATCH COMPLETE")
        print(f"{'='*60}")
        print(f"Processed: {stats['processed']}")
        print(f"Failed: {stats['failed']}")
        print(f"Total: {stats['total']}")
        print(f"Duration: {duration:.1f}s")
        print(f"{'='*60}\n")
        
        return stats


# === MAIN BLOCK ===
if __name__ == "__main__":
    import json
    
    print("=== QUEUE CONSUMER TEST ===\n")
    
    # Consumer erstellen (human wrapper)
    consumer = QueueConsumer(wrapper_name="human")
    
    # Process 3 jobs als Test
    stats = consumer.process_batch(batch_size=3)
    
    print("\n=== FINAL STATS ===")
    print(json.dumps(stats, indent=2))
