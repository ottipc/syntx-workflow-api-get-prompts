#!/usr/bin/env python3
"""
inject_syntex_enhanced.py

SYNTEX::TRUE_RAW Enhanced - Mit Quality Scoring & Progress Tracking
"""

import argparse
import sys
from pathlib import Path

from syntex.core.calibrator_enhanced import EnhancedSyntexCalibrator
from syntex.analysis.tracker import ProgressTracker


def main():
    parser = argparse.ArgumentParser(
        description="SYNTEX::TRUE_RAW Enhanced - Semantische Resonanz-Kalibrierung mit Analytics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  # Standard Kalibrierung mit Quality Score
  python inject_syntex_enhanced.py -f prompts/test.txt
  
  # Ohne Quality-Ausgabe
  python inject_syntex_enhanced.py -f prompts/test.txt --no-quality
  
  # Progress Summary anzeigen
  python inject_syntex_enhanced.py --show-progress
  
  # Direkter Prompt
  python inject_syntex_enhanced.py -p "Erkläre emotionalen Rückzug"
        """
    )
    
    # Input
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        '-f', '--file',
        type=Path,
        help='Meta-Prompt aus Datei laden'
    )
    input_group.add_argument(
        '-p', '--prompt',
        type=str,
        help='Meta-Prompt direkt als String'
    )
    input_group.add_argument(
        '--show-progress',
        action='store_true',
        help='Zeige Progress Summary und beende'
    )
    
    # Optional
    parser.add_argument(
        '-w', '--wrapper',
        type=Path,
        default=Path('syntex_wrapper.txt'),
        help='Custom SYNTEX Wrapper Datei'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Keine Ausgabe im Terminal'
    )
    parser.add_argument(
        '--no-quality',
        action='store_true',
        help='Quality Score nicht anzeigen'
    )
    
    args = parser.parse_args()
    
    # Show Progress Mode
    if args.show_progress:
        tracker = ProgressTracker()
        print(tracker.format_summary(n=20))
        sys.exit(0)
    
    # Validierung
    if not args.file and not args.prompt:
        parser.print_help()
        sys.exit(1)
    
    # Meta-Prompt laden
    if args.file:
        if not args.file.exists():
            print(f"❌ Datei nicht gefunden: {args.file}", file=sys.stderr)
            sys.exit(1)
        
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                meta_prompt = f.read().strip()
        except Exception as e:
            print(f"❌ Fehler beim Lesen der Datei: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        meta_prompt = args.prompt.strip()
    
    if not meta_prompt:
        print("❌ Meta-Prompt ist leer", file=sys.stderr)
        sys.exit(1)
    
    # Enhanced Calibrator
    calibrator = EnhancedSyntexCalibrator(wrapper_file=args.wrapper)
    
    # Kalibrierung durchführen
    success, response, metadata = calibrator.calibrate(
        meta_prompt=meta_prompt,
        verbose=not args.quiet,
        show_quality=not args.no_quality
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
