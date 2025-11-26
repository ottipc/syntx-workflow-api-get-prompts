#!/usr/bin/env python3
"""
SYNTEX SIGMA Pipeline - für Training
Nutzt SIGMA-Wrapper statt menschlicher Terminologie
"""

import sys
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from gpt_generator.syntx_prompt_generator import generate_prompt
from gpt_generator.topics_database import TOPICS
from syntex.core.calibrator_enhanced import EnhancedSyntexCalibrator


def main():
    import argparse
    parser = argparse.ArgumentParser(description="SYNTEX SIGMA Training Pipeline")
    parser.add_argument('-b', '--batch', type=int, default=20, help='Anzahl Prompts')
    args = parser.parse_args()
    
    # Path-Objekt für Wrapper
    calibrator = EnhancedSyntexCalibrator(wrapper_name="sigma")
    
    # Random Topics
    all_topics = [topic for category in TOPICS.values() for topic in category]
    selected = random.sample(all_topics, min(args.batch, len(all_topics)))
    
    print(f"🔥 SIGMA Training Pipeline - {args.batch} Prompts")
    
    success_count = 0
    
    for i, topic in enumerate(selected, 1):
        print(f"\n[{i}/{args.batch}] {topic}")
        
        # GPT generiert
        gpt_result = generate_prompt(
            prompt=topic,
            style="technisch",
            max_tokens=250
        )
        
        if not gpt_result['success']:
            print(f"   ❌ GPT failed")
            continue
        
        meta_prompt = gpt_result['prompt_generated']
        
        # SYNTEX SIGMA Kalibrierung
        success, response, metadata = calibrator.calibrate(
            meta_prompt=meta_prompt,
            verbose=False,
            show_quality=False
        )
        
        if success:
            quality = metadata.get('quality_score', {}).get('total_score', 0)
            print(f"   ✅ Score: {quality}/100")
            success_count += 1
        else:
            print(f"   ❌ Failed")
    
    print(f"\n{'='*80}")
    print(f"SIGMA Training Session Complete")
    print(f"Success: {success_count}/{args.batch}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
