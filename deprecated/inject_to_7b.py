#!/usr/bin/env python3
"""
inject_to_7b.py
Injiziert fertige Prompts in das lokale 7B-Modell und loggt die Ergebnisse.
"""

import argparse
import json
import time
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

import requests


# ============================================================================
# KONFIGURATION
# ============================================================================

API_ENDPOINT = "https://dev.syntx-system.com/api/chat"
LOG_FILE = Path("logs/7b_injections.jsonl")
MAX_RETRIES = 3
RETRY_DELAYS = [1, 3, 7]  # Exponential Backoff in Sekunden
CONNECT_TIMEOUT = 30
READ_TIMEOUT = 120
MAX_PROMPT_LENGTH = 8192  # Warnung bei längeren Prompts


# ============================================================================
# LOGGING
# ============================================================================

def write_log(log_entry: Dict[str, Any]) -> None:
    """Schreibt einen Log-Eintrag in die JSONL-Datei."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')


def create_log_entry(
    prompt: str,
    response: Optional[str],
    success: bool,
    duration_ms: int,
    retry_count: int,
    error: Optional[str] = None,
    warning: Optional[str] = None
) -> Dict[str, Any]:
    """Erstellt einen strukturierten Log-Eintrag."""
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "endpoint": API_ENDPOINT,
        "prompt_length": len(prompt),
        "prompt_preview": prompt[:200] + "..." if len(prompt) > 200 else prompt,
        "response": response,
        "success": success,
        "error": error,
        "warning": warning,
        "duration_ms": duration_ms,
        "retry_count": retry_count
    }


# ============================================================================
# API KOMMUNIKATION
# ============================================================================

def send_to_7b(
    prompt: str,
    max_new_tokens: int = 512,
    temperature: float = 0.7,
    top_p: float = 0.9,
    do_sample: bool = True
) -> tuple[Optional[str], Optional[str], int]:
    """
    Sendet Prompt an das 7B-Modell mit Retry-Logik.
    
    Returns:
        (response_text, error_message, retry_count)
    """
    payload = {
        "prompt": prompt,
        "max_new_tokens": max_new_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "do_sample": do_sample
    }
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                API_ENDPOINT,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
            )
            
            # HTTP-Fehler prüfen
            if response.status_code >= 500:
                raise requests.HTTPError(f"Server Error {response.status_code}: {response.text}")
            
            response.raise_for_status()
            
            # JSON parsen
            result = response.json()
            
            # Response extrahieren
            if "response" not in result:
                raise ValueError(f"Unexpected response format: {result}")
            
            return result["response"], None, attempt
            
        except requests.Timeout as e:
            error_msg = f"Timeout after {CONNECT_TIMEOUT}s connect / {READ_TIMEOUT}s read"
            if attempt < MAX_RETRIES - 1:
                print(f"⚠️  Attempt {attempt + 1} failed: {error_msg}. Retrying in {RETRY_DELAYS[attempt]}s...", file=sys.stderr)
                time.sleep(RETRY_DELAYS[attempt])
            else:
                return None, error_msg, attempt
                
        except requests.ConnectionError as e:
            error_msg = f"Connection failed: {str(e)}"
            if attempt < MAX_RETRIES - 1:
                print(f"⚠️  Attempt {attempt + 1} failed: {error_msg}. Retrying in {RETRY_DELAYS[attempt]}s...", file=sys.stderr)
                time.sleep(RETRY_DELAYS[attempt])
            else:
                return None, error_msg, attempt
                
        except requests.HTTPError as e:
            error_msg = f"HTTP Error: {str(e)}"
            if attempt < MAX_RETRIES - 1 and response.status_code >= 500:
                print(f"⚠️  Attempt {attempt + 1} failed: {error_msg}. Retrying in {RETRY_DELAYS[attempt]}s...", file=sys.stderr)
                time.sleep(RETRY_DELAYS[attempt])
            else:
                return None, error_msg, attempt
                
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON response: {str(e)}"
            return None, error_msg, attempt
            
        except Exception as e:
            error_msg = f"Unexpected error: {type(e).__name__}: {str(e)}"
            return None, error_msg, attempt
    
    return None, "Max retries exceeded", MAX_RETRIES - 1


# ============================================================================
# HAUPTLOGIK
# ============================================================================

def inject_prompt(prompt_file: Path) -> bool:
    """
    Liest Prompt aus Datei, sendet ihn an 7B und loggt das Ergebnis.
    
    Returns:
        True bei Erfolg, False bei Fehler
    """
    # Prompt-Datei lesen
    if not prompt_file.exists():
        print(f"❌ Fehler: Datei nicht gefunden: {prompt_file}", file=sys.stderr)
        return False
    
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt = f.read().strip()
    except Exception as e:
        print(f"❌ Fehler beim Lesen der Datei: {e}", file=sys.stderr)
        return False
    
    if not prompt:
        print(f"❌ Fehler: Prompt-Datei ist leer", file=sys.stderr)
        return False
    
    # Warnung bei zu langen Prompts
    warning = None
    if len(prompt) > MAX_PROMPT_LENGTH:
        warning = f"Prompt exceeds recommended length: {len(prompt)} > {MAX_PROMPT_LENGTH} chars"
        print(f"⚠️  {warning}", file=sys.stderr)
    
    # An 7B senden
    print(f"📤 Sende Prompt ({len(prompt)} Zeichen) an {API_ENDPOINT}...")
    start_time = time.time()
    
    response_text, error_msg, retry_count = send_to_7b(prompt)
    
    duration_ms = int((time.time() - start_time) * 1000)
    
    # Log erstellen
    log_entry = create_log_entry(
        prompt=prompt,
        response=response_text,
        success=(error_msg is None),
        duration_ms=duration_ms,
        retry_count=retry_count,
        error=error_msg,
        warning=warning
    )
    
    write_log(log_entry)
    
    # Ausgabe
    if error_msg:
        print(f"❌ Fehler nach {retry_count + 1} Versuchen: {error_msg}", file=sys.stderr)
        print(f"📝 Log geschrieben: {LOG_FILE}", file=sys.stderr)
        return False
    else:
        print(f"✅ Erfolg nach {retry_count + 1} Versuch(en) ({duration_ms}ms)")
        print(f"\n📥 Response:\n{response_text}\n")
        print(f"📝 Log geschrieben: {LOG_FILE}")
        return True


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Injiziert fertige Prompts in das lokale 7B-Modell",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  python inject_to_7b.py --prompt-file prompts/prompt_2025-11-25-1845.txt
  python inject_to_7b.py -f test_prompt.txt
        """
    )
    
    parser.add_argument(
        '-f', '--prompt-file',
        type=Path,
        required=True,
        help='Pfad zur Prompt-Datei'
    )
    
    args = parser.parse_args()
    
    success = inject_prompt(args.prompt_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
