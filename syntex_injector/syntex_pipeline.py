#!/usr/bin/env python3
"""
syntex_pipeline.py

Vollständige Pipeline: GPT-4 → SYNTEX → Llama → Analytics
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Optional, Dict, List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from gpt_generator.syntx_prompt_generator import generate_prompt
from syntex.core.calibrator_enhanced import EnhancedSyntexCalibrator


class SyntexPipeline:
    """
    End-to-End Pipeline für SYNTEX-Kalibrierung
    
    Flow:
    1. GPT-4 generiert Meta-Prompt
    2. SYNTEX Wrapper hinzufügen
    3. Llama kalibriert
    4. Combined Analytics
    """
    
    def __init__(self):
        self.calibrator = EnhancedSyntexCalibrator()
        self.results = []
    
    def run_single(
        self,
        topic: str,
        style: str = "technisch",
        verbose: bool = True
    ) -> Dict:
        """
        Führt komplette Pipeline für ein Topic durch.
        
        Returns:
            Combined result mit GPT + Llama Metriken
        """
        if verbose:
            print(f"\n{'='*80}")
            print(f"SYNTEX PIPELINE: {topic}")
            print(f"Style: {style}")
            print(f"{'='*80}\n")
        
        # 1. GPT-4 generiert Meta-Prompt
        if verbose:
            print("🤖 GPT-4: Generiere Meta-Prompt...")
        
        gpt_result = generate_prompt(
            prompt=topic,
            style=style,
            max_tokens=200,
            max_refusal_retries=3,
            category="technologie"
        )
        
        if not gpt_result['success']:
            return {
                "success": False,
                "error": "GPT-4 generation failed",
                "gpt_result": gpt_result
            }
        
        meta_prompt = gpt_result['prompt_generated']
        
        if verbose:
            print(f"✅ GPT-4 Done ({gpt_result['duration_ms']}ms)")
            print(f"   Quality: {gpt_result['quality_score']['total_score']}/10")
            print(f"   Cost: ${gpt_result['cost']['total_cost']:.6f}")
            print(f"   Meta-Prompt: {len(meta_prompt)} Zeichen\n")
        
        # 2. SYNTEX Kalibrierung
        if verbose:
            print("🔧 SYNTEX: Kalibriere mit Llama...")
        
        success, response, metadata = self.calibrator.calibrate(
            meta_prompt=meta_prompt,
            verbose=verbose,
            show_quality=verbose
        )
        
        # 3. Combined Result
        result = {
            "success": success,
            "topic": topic,
            "style": style,
            "gpt": {
                "meta_prompt": meta_prompt,
                "quality_score": gpt_result['quality_score'],
                "cost": gpt_result['cost'],
                "duration_ms": gpt_result['duration_ms']
            },
            "syntex": {
                "response": response,
                "quality_score": metadata.get('quality_score'),
                "duration_ms": metadata['duration_ms'],
                "session_id": metadata['session_id']
            },
            "total_duration_ms": gpt_result['duration_ms'] + metadata['duration_ms'],
            "total_cost_usd": gpt_result['cost']['total_cost']
        }
        
        self.results.append(result)
        return result
    
    def run_batch(
        self,
        topics: List[str],
        styles: Optional[List[str]] = None,
        verbose: bool = True
    ) -> List[Dict]:
        """Führt Pipeline für mehrere Topics durch"""
        if styles is None:
            styles = ["technisch"] * len(topics)
        
        results = []
        for i, (topic, style) in enumerate(zip(topics, styles), 1):
            if verbose:
                print(f"\n[{i}/{len(topics)}] Processing: {topic}")
            
            result = self.run_single(topic, style, verbose)
            results.append(result)
        
        return results
    
    def format_summary(self, results: List[Dict]) -> str:
        """Formatiert Batch-Zusammenfassung"""
        if not results:
            return "Keine Ergebnisse"
        
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        # Durchschnitte
        avg_gpt_quality = sum(r['gpt']['quality_score']['total_score'] for r in successful) / len(successful) if successful else 0
        avg_syntex_quality = sum(r['syntex']['quality_score']['total_score'] for r in successful if r['syntex']['quality_score']) / len(successful) if successful else 0
        total_cost = sum(r['total_cost_usd'] for r in successful)
        avg_duration = sum(r['total_duration_ms'] for r in successful) / len(successful) if successful else 0
        
        output = []
        output.append(f"\n{'='*80}")
        output.append(f"SYNTEX PIPELINE SUMMARY")
        output.append(f"{'='*80}")
        output.append(f"Total: {len(results)}")
        output.append(f"✅ Success: {len(successful)} ({len(successful)/len(results)*100:.1f}%)")
        output.append(f"❌ Failed: {len(failed)}")
        output.append(f"\n📊 Quality:")
        output.append(f"   GPT-4 Avg: {avg_gpt_quality:.1f}/10")
        output.append(f"   SYNTEX Avg: {avg_syntex_quality:.1f}/100")
        output.append(f"\n⏱️  Performance:")
        output.append(f"   Avg Duration: {avg_duration/1000:.1f}s")
        output.append(f"\n💰 Costs:")
        output.append(f"   Total: ${total_cost:.4f}")
        output.append(f"   Per Item: ${total_cost/len(successful):.4f}" if successful else "   -")
        output.append(f"{'='*80}\n")
        
        return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="SYNTEX Pipeline: GPT-4 → SYNTEX → Llama",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-t', '--topic',
        type=str,
        help='Einzelnes Topic'
    )
    parser.add_argument(
        '-b', '--batch',
        type=int,
        help='Anzahl Random Topics'
    )
    parser.add_argument(
        '-s', '--style',
        type=str,
        default='technisch',
        choices=['technisch', 'kreativ', 'akademisch', 'casual'],
        help='Prompt Style'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Minimale Ausgabe'
    )
    
    args = parser.parse_args()
    
    pipeline = SyntexPipeline()
    
    if args.topic:
        # Single Topic
        result = pipeline.run_single(
            topic=args.topic,
            style=args.style,
            verbose=not args.quiet
        )
        sys.exit(0 if result['success'] else 1)
    
    elif args.batch:
        # Batch Random Topics
        from gpt_generator.topics_database import TOPICS
        import random
        
        all_topics = [topic for category in TOPICS.values() for topic in category]
        selected = random.sample(all_topics, min(args.batch, len(all_topics)))
        
        results = pipeline.run_batch(
            topics=selected,
            verbose=not args.quiet
        )
        
        if not args.quiet:
            print(pipeline.format_summary(results))
        
        sys.exit(0)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
