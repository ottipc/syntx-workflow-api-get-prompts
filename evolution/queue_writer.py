"""
SYNTX Queue Writer
Schreibt generierte Prompts in queue/incoming/
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config_loader import get_config


class QueueWriter:
    """Schreibt Prompts atomic in queue/incoming/"""
    
    def __init__(self):
        self.queue_base = Path(get_config('queue', 'paths', 'base'))
        self.incoming_dir = self.queue_base / "incoming"
        self.tmp_dir = self.queue_base / ".tmp"
        
        # Ensure directories exist
        self.incoming_dir.mkdir(parents=True, exist_ok=True)
        self.tmp_dir.mkdir(parents=True, exist_ok=True)
    
    def write_prompt(self, prompt_result: Dict[str, Any]) -> bool:
        """
        Schreibt einen generierten Prompt in queue/incoming/
        
        Args:
            prompt_result: Output von generate_prompt()
            
        Returns:
            True wenn erfolgreich
        """
        if not prompt_result.get('success'):
            return False
        
        # Filename erstellen
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        topic = prompt_result.get('category', 'unknown')
        style = prompt_result.get('style', 'unknown')
        
        filename = f"{timestamp}__topic_{topic}__style_{style}"
        
        # TXT File (der generierte Prompt)
        txt_file = self.tmp_dir / f"{filename}.txt"
        json_file = self.tmp_dir / f"{filename}.json"
        
        # Write TXT
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(prompt_result['prompt_generated'])
        
        # Write JSON (Metadata)
        metadata = {
            'topic': prompt_result.get('category'),
            'style': prompt_result.get('style'),
            'language': prompt_result.get('language', 'de'),
            'category': prompt_result.get('category'),
            'gpt_quality': prompt_result.get('quality_score'),
            'gpt_cost': prompt_result.get('cost'),
            'model': prompt_result.get('model'),
            'duration_ms': prompt_result.get('duration_ms'),
            'producer_run': datetime.now().isoformat(),
            'created_at': datetime.now().isoformat(),
            'filename': f"{filename}.txt"
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        # Atomic move zu incoming/
        txt_target = self.incoming_dir / f"{filename}.txt"
        json_target = self.incoming_dir / f"{filename}.json"
        
        txt_file.rename(txt_target)
        json_file.rename(json_target)
        
        return True
    
    def write_batch(self, results: list) -> Dict[str, int]:
        """
        Schreibt einen Batch von Prompts
        
        Returns:
            {'written': N, 'failed': M}
        """
        written = 0
        failed = 0
        
        for result in results:
            if self.write_prompt(result):
                written += 1
            else:
                failed += 1
        
        return {'written': written, 'failed': failed}


if __name__ == "__main__":
    print("📝 Queue Writer Test\n")
    
    # Mock prompt result
    mock_result = {
        'success': True,
        'prompt_generated': 'Test prompt content here...',
        'category': 'test',
        'style': 'casual',
        'language': 'de',
        'quality_score': {'total_score': 8},
        'cost': {'total_cost': 0.001},
        'model': 'gpt-4o',
        'duration_ms': 1000
    }
    
    writer = QueueWriter()
    success = writer.write_prompt(mock_result)
    
    if success:
        print("✅ Test prompt written to queue/incoming/")
        
        # Check
        import os
        count = len([f for f in os.listdir(writer.incoming_dir) if f.endswith('.txt')])
        print(f"✅ Queue has {count} prompts")
    else:
        print("❌ Failed to write")
