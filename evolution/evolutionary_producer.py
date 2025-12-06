"""
SYNTX Evolutionary Producer
Self-Optimizing GPT-4 Generator mit Field-Based Learning + Queue Integration
"""
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import os
from dotenv import load_dotenv
import random
# Load environment variables
load_dotenv(override=True)

sys.path.insert(0, str(Path(__file__).parent.parent))

from evolution.field_analyzer import FieldAnalyzer
from evolution.pattern_learner import PatternLearner
from evolution.queue_writer import QueueWriter
from config.config_loader import get_config

# Import GPT Generator
sys.path.insert(0, str(Path(__file__).parent.parent / "gpt_generator"))
from gpt_generator.syntx_prompt_generator import generate_prompt
from gpt_generator.topics_database import get_random_topics
from gpt_generator.prompt_styles import get_all_styles


class EvolutionaryProducer:
    """
    Self-Optimizing Producer mit SYNTX Field-Based Learning
    
    Flow:
    1. Analysiere processed/ Jobs (FieldAnalyzer)
    2. Lerne erfolgreiche Patterns (PatternLearner)
    3. Generiere optimierte Prompts (GPT-4 mit Meta-Prompts)
    4. Schreibe in queue/incoming/ (QueueWriter)
    5. Archiviere gelernte Jobs
    6. Logge Evolution
    """
    
    def __init__(self):
        self.analyzer = FieldAnalyzer()
        self.learner = PatternLearner()
        self.writer = QueueWriter()
        self.config = get_config('evolution')
        
        # Settings
        self.batch_size = get_config('evolution', 'producer', 'generation', 'batch_size', default=20)
        self.learning_enabled = get_config('evolution', 'producer', 'learning', 'enabled', default=True)
        self.max_samples = get_config('evolution', 'producer', 'learning', 'max_samples', default=50)
        self.min_score = get_config('evolution', 'producer', 'learning', 'min_score', default=90)
        self.archive_after_read = get_config('evolution', 'producer', 'learning', 'archive_after_read', default=True)
        
        self.generation = self._get_current_generation()
    
    def _get_current_generation(self) -> int:
        """Ermittelt aktuelle Generation aus Logs"""
        log_dir = Path(get_config('generator', 'logging', 'base_dir'))
        evo_log = log_dir / get_config('evolution', 'logging', 'evolution_log')
        
        if not evo_log.exists():
            return 1
        
        # Letzte Generation aus Log
        try:
            with open(evo_log, 'r') as f:
                lines = f.readlines()
                if lines:
                    import json
                    last = json.loads(lines[-1])
                    return last.get('generation', 0) + 1
        except:
            pass
        
        return 1
    
    def run(self) -> Dict[str, Any]:
        """
        Hauptlogik: Learn → Generate → Write to Queue → Archive → Log
        
        Returns:
            Stats dict
        """
        print(f"\n{'='*60}")
        print(f"🧬 SYNTX EVOLUTIONARY PRODUCER - Generation {self.generation}")
        print(f"{'='*60}\n")
        
        # PHASE 1: LEARNING
        analysis = None
        learned_jobs = []
        
        if self.learning_enabled:
            print("📚 PHASE 1: LEARNING FROM PROCESSED/")
            learned_jobs = self.analyzer.get_top_processed_jobs(
                max_samples=self.max_samples,
                min_score=self.min_score
            )
            
            if learned_jobs:
                print(f"   ✅ Found {len(learned_jobs)} high-quality jobs (score >= {self.min_score})")
                analysis = self.analyzer.analyze_patterns(learned_jobs)
                
                print(f"   📊 Avg Score: {analysis['avg_score']}/100")
                print(f"   📊 Patterns: {len(analysis['patterns'])} detected")
                print()
            else:
                print(f"   ℹ️  No jobs with score >= {self.min_score} found")
                print(f"   ℹ️  Generation {self.generation} will explore without learning\n")
        
        # PHASE 2: GENERATION
        print(f"🎨 PHASE 2: GENERATING {self.batch_size} OPTIMIZED PROMPTS")
        
        # Topics holen
        topics = get_random_topics(self.batch_size)
        styles = get_all_styles()
        
        results = []
        successful = 0
        
        for i, (category, topic) in enumerate(topics, 1):
            # Style wählen (aus Patterns wenn vorhanden)
            if analysis and analysis['sample_count'] > 0:
                # Nutze erfolgreiche Styles
                top_styles = list(analysis['styles'].keys())[:3]
                style = random.choice(top_styles) if top_styles else random.choice(styles)
            else:
                style = random.choice(styles)
            
            print(f"   [{i}/{self.batch_size}] {category}: {topic} ({style})")
            
            # Meta-Prompt erstellen wenn Learning aktiv
            if analysis and analysis['sample_count'] > 0:
                meta_prompt = self.learner.create_meta_prompt(analysis, topic, style)
                # Nutze optimierten Meta-Prompt
                result = generate_prompt(
                    prompt=meta_prompt,
                    style=style,
                    category=category,
                    max_tokens=500
                )
            else:
                # Normaler Prompt ohne Learning
                result = generate_prompt(
                    prompt=topic,
                    style=style,
                    category=category,
                    max_tokens=500
                )
            
            results.append(result)
            
            if result['success']:
                successful += 1
                quality = result.get('quality_score', {}).get('total_score', 0)
                print(f"        ✅ Generated (GPT Quality: {quality}/10)")
            else:
                print(f"        ❌ Failed: {result.get('error', 'Unknown')}")
        
        print()
        
        # PHASE 3: WRITE TO QUEUE
        print(f"📝 PHASE 3: WRITING {successful} PROMPTS TO QUEUE")
        write_stats = self.writer.write_batch(results)
        print(f"   ✅ Written: {write_stats['written']} to queue/incoming/")
        if write_stats['failed'] > 0:
            print(f"   ⚠️  Failed: {write_stats['failed']}")
        print()
        
        # PHASE 4: ARCHIVE
        archived = 0
        if self.archive_after_read and learned_jobs:
            print(f"📦 PHASE 4: ARCHIVING {len(learned_jobs)} LEARNED JOBS")
            archived = self.analyzer.archive_processed_jobs(learned_jobs)
            print(f"   ✅ Archived {archived} jobs to archive/\n")
        
        # PHASE 5: LOG EVOLUTION
        if analysis:
            print("📊 PHASE 5: LOGGING EVOLUTION")
            self.learner.log_evolution(
                generation=self.generation,
                analysis=analysis,
                prompts_generated=successful
            )
            print(f"   ✅ Logged to evolution.jsonl\n")
        
        # Summary
        stats = {
            'generation': self.generation,
            'learned_from': len(learned_jobs),
            'generated': self.batch_size,
            'successful': successful,
            'failed': self.batch_size - successful,
            'written_to_queue': write_stats['written'],
            'archived': archived,
            'learning_enabled': self.learning_enabled,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"{'='*60}")
        print(f"📊 GENERATION {self.generation} SUMMARY:")
        print(f"   Learned from: {stats['learned_from']} jobs")
        print(f"   Generated: {stats['successful']}/{stats['generated']} successful")
        print(f"   Written to Queue: {stats['written_to_queue']}")
        print(f"   Archived: {stats['archived']} jobs")
        print(f"{'='*60}\n")
        
        return stats


if __name__ == "__main__":
    producer = EvolutionaryProducer()
    stats = producer.run()
    
    print("✅ Evolutionary Producer completed!")
    print(f"   Generation: {stats['generation']}")
    print(f"   Success Rate: {stats['successful']}/{stats['generated']}")
    print(f"   Queue: {stats['written_to_queue']} prompts ready for Consumer")
