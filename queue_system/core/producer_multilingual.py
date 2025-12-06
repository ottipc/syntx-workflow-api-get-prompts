"""
SYNTX Multilingual Producer

=== NEUERUNG ===
Producer wählt zufällige Sprache für jedes Prompt
GPT bekommt Language Instruction
Metadata wird gespeichert

=== FLOW ===
1. Choose Language (weighted random)
2. Generate Prompt mit Language Annotation
3. Save mit Language Metadata
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import random

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from queue_system.core.language_rotation import rotator, Language
from queue_system.core.queue_manager import QueueManager
from queue_system.core.file_handler import FileHandler
from gpt_generator.topics_database import get_random_topics

# Import OpenAI for direct generation
from openai import OpenAI


class MultilingualProducer:
    """
    Producer mit Language Rotation
    
    === LOGIK ===
    - Wählt Sprache per Weighted Random
    - Annotiert Prompt mit Sprachhinweis
    - Speichert Language Metadata
    """
    
    def __init__(self):
        self.queue_manager = QueueManager()
        self.file_handler = FileHandler()
        self.rotator = rotator
        self.client = OpenAI()
        
    def run(self, force: bool = False, count: Optional[int] = None) -> Dict:
        """
        Hauptlogik: Generate prompts mit Language Rotation
        
        Args:
            force: Ignoriert Queue-Check
            count: Override batch size
        """
        start_time = datetime.now()
        
        # Decision Phase
        if not force:
            should_produce, batch_size = self.queue_manager.should_produce()
            if not should_produce:
                return {
                    "should_produce": False,
                    "skipped": True,
                    "reason": "Queue sufficient"
                }
        else:
            batch_size = count or 20
        
        print(f"\n🌍 MULTILINGUAL PRODUCER")
        print(f"🔧 Generiere {batch_size} Prompts mit Language Rotation...")
        print()
        
        # Production Phase
        produced = 0
        failed = 0
        language_stats = {}
        
        for i, (topic, category) in enumerate(get_random_topics(batch_size), 1):
            # Choose Language
            language = self.rotator.choose_language()
            language_stats[language.code] = language_stats.get(language.code, 0) + 1
            
            # Language Instruction for GPT
            lang_instruction = self._get_language_instruction(language)
            
            # Generate Prompt
            style = self._choose_style()
            
            try:
                result = self._generate_prompt(
                    topic=topic,
                    language=language,
                    style=style
                )
                
                if result['success']:
                    # Save to Queue mit Language Metadata
                    metadata = {
                        'topic': topic,
                        'style': style,
                        'category': category,
                        'language': language.code,
                        'language_name': language.name,
                        'language_instruction': lang_instruction,
                        'gpt_quality': result.get('quality_score', {}),
                        'gpt_cost': result.get('cost', {}),
                        'producer_run': datetime.now().isoformat(),
                        'multilingual': True
                    }
                    
                    self.file_handler.atomic_write(
                        content=result['prompt_generated'],
                        metadata=metadata,
                        target_dir=Path('queue/incoming')
                    )
                    
                    produced += 1
                    print(f"[{i}/{batch_size}] {category}: {topic}")
                    print(f"   🌍 Language: {language.code.upper()} ({language.name})")
                    print(f"   ✅ In Queue geschrieben")
                else:
                    failed += 1
                    print(f"[{i}/{batch_size}] ❌ Failed: {result.get('error', 'Unknown')}")
            except Exception as e:
                failed += 1
                print(f"[{i}/{batch_size}] ❌ Exception: {str(e)}")
        
        duration = (datetime.now() - start_time).total_seconds()
        
        print(f"\n✅ Production Complete:")
        print(f"   Success: {produced}/{batch_size}")
        print(f"   Failed: {failed}")
        print(f"   Duration: {duration:.1f}s")
        print(f"\n📊 Language Distribution:")
        for lang_code, count in sorted(language_stats.items(), key=lambda x: -x[1]):
            lang = self.rotator.get_language(lang_code)
            print(f"   {lang_code.upper()} ({lang.name}): {count}")
        
        return {
            "should_produce": True,
            "requested_count": batch_size,
            "produced_count": produced,
            "failed_count": failed,
            "duration_seconds": duration,
            "language_stats": language_stats
        }
    
    def _generate_prompt(self, topic: str, language: Language, style: str) -> Dict:
        """
        Generate prompt with GPT in specified language
        """
        lang_instruction = self._get_language_instruction(language)
        
        system_prompt = f"""You are a creative prompt generator for SYNTX calibration.
Generate a meta-prompt in {language.name} that asks about: {topic}
Style: {style}
The prompt should be clear and engaging."""
        
        user_prompt = f"{lang_instruction} {topic}"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.8
            )
            
            prompt_text = response.choices[0].message.content
            
            return {
                'success': True,
                'prompt_generated': prompt_text,
                'quality_score': {'total': 8},  # Placeholder
                'cost': {
                    'input_tokens': response.usage.prompt_tokens,
                    'output_tokens': response.usage.completion_tokens,
                    'total_cost': 0.001  # Approximate
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_language_instruction(self, language: Language) -> str:
        """
        Generiere Language Instruction für GPT
        """
        instructions = {
            "de": "Erkläre auf Deutsch:",
            "en": "Explain in English:",
            "ru": "Объясни на русском:",
            "hu": "Magyarázd el magyarul:",
            "tr": "Türkçe açıkla:",
            "it": "Spiega in italiano:"
        }
        return instructions.get(language.code, "Explain:")
    
    def _choose_style(self) -> str:
        """Choose random style"""
        styles = ['casual', 'akademisch', 'technisch', 'kreativ']
        return random.choice(styles)


if __name__ == "__main__":
    print("=== MULTILINGUAL PRODUCER TEST ===\n")
    
    producer = MultilingualProducer()
    
    # Test with 5 prompts
    stats = producer.run(force=True, count=5)
    
    print("\n=== STATS ===")
    import json
    print(json.dumps(stats, indent=2, ensure_ascii=False))
