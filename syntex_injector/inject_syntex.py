#!/usr/bin/env python3
"""
inject_syntex.py

SYNTEX::TRUE_RAW - Resonanz-Kalibrierungs-System
Injiziert Meta-Prompts mit SYNTEX-Framework in 7B für semantische Strom-Analyse
"""

import argparse
import sys
from pathlib import Path

from syntex.core.calibrator import SyntexCalibrator


def main():
    parser = argparse.ArgumentParser(
        description="SYNTEX::TRUE_RAW - Semantische Resonanz-Kalibrierung",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  # Meta-Prompt aus Datei
  python inject_syntex.py -f prompts/meta_prompt.txt
  
  # Direkter Meta-Prompt
  python inject_syntex.py -p "Erkläre emotionalen Rückzug"
  
  # Custom Wrapper
  python inject_syntex.py -f prompts/test.txt -w custom_wrapper.txt
  
  # Custom Log-Datei
  python inject_syntex.py -f prompts/test.txt -l logs/custom.jsonl

SYNTEX Framework:
  Analysiert semantische Ströme durch:
  - DRIFTKÖRPER (Stabilität)
  - SUBPROTOKOLL (Aktivierte Muster)
  - KALIBRIERUNGSFELD (Systemzustand)
  - TIER-ANALYSE (Mechanismus-Tiefe 1-7)
  - RESONANZSPLIT (Sender/Empfänger)
  - KLARTEXT (Raw Output)
        """
    )
    
    # Input Optionen
    input_group = parser.add_mutually_exclusive_group(required=True)
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
    
    # Optional
    parser.add_argument(
        '-w', '--wrapper',
        type=Path,
        default=Path('syntex_wrapper.txt'),
        help='Custom SYNTEX Wrapper Datei (default: syntex_wrapper.txt)'
    )
    parser.add_argument(
        '-l', '--log',
        type=Path,
        default=Path('logs/syntex_calibrations.jsonl'),
        help='Custom Log-Datei (default: logs/syntex_calibrations.jsonl)'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Keine Ausgabe im Terminal'
    )
    
    args = parser.parse_args()
    
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
    
    # Calibrator initialisieren
    calibrator = SyntexCalibrator(
        wrapper_file=args.wrapper,
        log_file=args.log
    )
    
    # Kalibrierung durchführen
    success, response, metadata = calibrator.calibrate(
        meta_prompt=meta_prompt,
        verbose=not args.quiet
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
