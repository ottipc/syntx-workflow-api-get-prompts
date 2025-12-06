"""
File Handler - Atomic File Operations für Queue
[... ALLE KOMMENTARE BLEIBEN GLEICH ...]
"""
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Union

from ..config.queue_config import *

# Job Type Hint (forward reference)
try:
    from .consumer import Job
except ImportError:
    Job = None


class FileHandler:
    """[... KOMMENTARE BLEIBEN ...]"""
    
    def atomic_write(self, content: str, metadata: Dict[str, Any], target_dir: Path) -> Path:
        """[... BLEIBT GLEICH ...]"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        topic_slug = self._slugify(metadata.get('topic', 'unknown'))[:30]
        style = metadata.get('style', 'unknown')
        filename = f"{timestamp}__topic_{topic_slug}__style_{style}.txt"
        
        temp_path = QUEUE_TMP / filename
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        meta_path = temp_path.with_suffix('.json')
        with open(meta_path, 'w', encoding='utf-8') as f:
            metadata['created_at'] = datetime.now().isoformat()
            metadata['filename'] = filename
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        final_path = target_dir / filename
        final_meta = final_path.with_suffix('.json')
        
        temp_path.rename(final_path)
        meta_path.rename(final_meta)
        
        return final_path
    
    def move_to_processed(self, job) -> Path:
        """[... KOMMENTAR BLEIBT ...]"""
        # Handle both Job object and Path
        if hasattr(job, 'file_path'):
            # Job object
            job_path = job.file_path
            meta_path = job.meta_path
            metadata = job.metadata
        else:
            # Plain Path
            job_path = job
            meta_path = job_path.with_suffix('.json')
            if meta_path.exists():
                with open(meta_path, 'r') as f:
                    metadata = json.load(f)
            else:
                metadata = {}
        
        target = QUEUE_PROCESSED / job_path.name
        target_meta = target.with_suffix('.json')
        
        metadata['processed_at'] = datetime.now().isoformat()
        metadata['status'] = 'success'
        
        with open(meta_path, 'w') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        job_path.rename(target)
        if meta_path.exists():
            meta_path.rename(target_meta)
        
        return target
    
    def move_to_error(self, job, error_info: Dict[str, Any]) -> Path:
        """[... KOMMENTAR BLEIBT ...]"""
        # Handle both Job object and Path
        if hasattr(job, 'file_path'):
            # Job object
            job_path = job.file_path
            meta_path = job.meta_path
            metadata = job.metadata.copy()
        else:
            # Plain Path
            job_path = job
            meta_path = job_path.with_suffix('.json')
            if meta_path.exists():
                with open(meta_path, 'r') as f:
                    metadata = json.load(f)
            else:
                metadata = {}
        
        retry_count = metadata.get('retry_count', 0) + 1
        metadata['retry_count'] = retry_count
        metadata['last_error'] = error_info
        metadata['failed_at'] = datetime.now().isoformat()
        metadata['status'] = 'error'
        
        base = job_path.stem
        new_filename = f"{base}__retry{retry_count}.txt"
        
        target = QUEUE_ERROR / new_filename
        target_meta = target.with_suffix('.json')
        
        with open(meta_path, 'w') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        job_path.rename(target)
        meta_path.rename(target_meta)
        
        return target
    
    def _slugify(self, text: str) -> str:
        """[... BLEIBT GLEICH ...]"""
        text = text.lower()
        replacements = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss', ' ': '_', '-': '_'}
        for old, new in replacements.items():
            text = text.replace(old, new)
        allowed = 'abcdefghijklmnopqrstuvwxyz0123456789_'
        text = ''.join(c for c in text if c in allowed)
        return text
