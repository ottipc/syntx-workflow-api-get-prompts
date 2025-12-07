"""
SYNTX Log Loader - FIXED
Liest aus queue/processed/*.json
"""

import json
from pathlib import Path
from typing import List, Dict, Optional

QUEUE_DIR = Path("/opt/syntx-workflow-api-get-prompts/queue")

def load_field_flow(limit: Optional[int] = None) -> List[Dict]:
    """Load from queue/processed/*.json"""
    processed_dir = QUEUE_DIR / "processed"
    
    if not processed_dir.exists():
        return []
    
    entries = []
    for json_file in sorted(processed_dir.glob("*.json")):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                
                # Transform to expected format
                entry = {
                    "job_id": data.get('filename', json_file.stem),
                    "topic": data.get('topic', 'unknown'),
                    "style": data.get('style', 'unknown'),
                    "category": data.get('category', 'unknown'),
                    "wrapper": data.get('syntex_result', {}).get('wrapper', 'unknown'),
                    "quality_score": data.get('syntex_result', {}).get('quality_score', {}),
                    "duration_ms": data.get('syntex_result', {}).get('duration_ms'),
                    "session_id": data.get('syntex_result', {}).get('session_id'),
                    "timestamp": data.get('processed_at', data.get('created_at')),
                    "status": data.get('status', 'unknown')
                }
                entries.append(entry)
        except Exception as e:
            continue
    
    if limit:
        return entries[-limit:]
    return entries

def load_evolution() -> List[Dict]:
    """Load evolution log"""
    evo_log = Path("/opt/syntx-config/logs/evolution.jsonl")
    if not evo_log.exists():
        return []
    
    entries = []
    try:
        with open(evo_log, 'r') as f:
            for line in f:
                try:
                    entries.append(json.loads(line.strip()))
                except:
                    continue
    except:
        pass
    return entries

def get_queue_counts() -> Dict[str, int]:
    """Get queue counts"""
    def count_files(subdir):
        p = QUEUE_DIR / subdir
        if not p.exists():
            return 0
        return len(list(p.glob("*.txt")))
    
    return {
        "incoming": count_files("incoming"),
        "processing": count_files("processing"),
        "processed": count_files("processed"),
        "error": count_files("error")
    }

# Exports
FIELD_FLOW_LOG = Path("/dev/null")  # Not used anymore
QUEUE_DIR = QUEUE_DIR
