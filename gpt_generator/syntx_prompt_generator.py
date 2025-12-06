import os
import json
import time
from datetime import datetime
from pathlib import Path
from openai import OpenAI, APIError, RateLimitError, APIConnectionError, APITimeoutError

# Import unserer neuen Module
from .prompt_scorer import score_prompt
from .cost_tracker import calculate_cost, save_cost_log
from .prompt_styles import apply_style


def log_request(log_data: dict) -> None:
    """Schreibt einen Log-Eintrag in die JSONL-Datei."""
    log_dir = Path("./logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / "gpt_prompts.jsonl"
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_data, ensure_ascii=False) + "\n")


def is_refusal(text: str) -> bool:
    """Prüft ob die Antwort eine Ablehnung ist."""
    if not text:
        return False
    
    refusal_patterns = [
        "es tut mir leid",
        "ich kann nicht",
        "ich kann bei dieser anfrage nicht helfen",
        "i cannot",
        "i can't",
        "i'm not able to",
        "i apologize, but",
        "i'm sorry, but"
    ]
    
    first_100 = text[:100].lower()
    return any(pattern in first_100 for pattern in refusal_patterns)


def generate_prompt(
    prompt: str, 
    temperature: float = 0.7, 
    top_p: float = 1.0, 
    max_tokens: int = 500, 
    max_refusal_retries: int = 3,
    style: str = None,
    category: str = None
) -> dict:
    """
    Generiert Prompts via OpenAI API mit Scoring und Cost-Tracking.
    
    Args:
        prompt: Der Steuer-Prompt oder Topic
        temperature: Temperatur (0.0 - 2.0)
        top_p: Top P (0.0 - 1.0)
        max_tokens: Maximale Token-Anzahl
        max_refusal_retries: Max. Versuche bei Refusals
        style: Prompt-Style (technisch, kreativ, akademisch, casual)
        
    Returns:
        dict mit success, prompt_sent, prompt_generated, error, model, duration_ms, 
             retries, refusal_attempts, quality_score, cost, style
    """
    
    # Style anwenden falls angegeben
    original_prompt = prompt
    if style:
        prompt = apply_style(prompt, style)
    
    # Eingabe validieren
    if not prompt or not prompt.strip():
        result = {
            "success": False,
            "prompt_sent": prompt,
            "prompt_generated": None,
            "error": "Empty input prompt",
            "model": "gpt-4o",
            "duration_ms": 0,
            "retries": 0,
            "refusal_attempts": 0,
            "quality_score": None,
            "cost": None,
            "style": style,
            "category": category
        }
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            **result,
            "retry_count": result["retries"]
        }
        log_request(log_entry)
        return result
    
    overall_start = datetime.now()
    refusal_attempt = 0
    current_prompt = prompt
    
    # Outer Loop: Refusal Retries
    while refusal_attempt <= max_refusal_retries:
        start_time = datetime.now()
        retry_count = 0
        max_retries = 3
        backoff_times = [1, 2, 4]
        
        # Inner Loop: Network/API Retries
        while retry_count <= max_retries:
            try:
                # OpenAI Client initialisieren
                client = OpenAI(timeout=45.0)
                
                # API Call
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "user", "content": current_prompt}
                    ],
                    temperature=temperature,
                    top_p=top_p,
                    max_tokens=max_tokens
                )
                
                # Response extrahieren
                generated_text = response.choices[0].message.content
                finish_reason = response.choices[0].finish_reason
                usage = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
                
                # Cost berechnen
                cost_info = calculate_cost(usage, "gpt-4o")
                save_cost_log(cost_info)
                
                # Quality Score berechnen
                quality = score_prompt(generated_text)
                
                # Check für Refusal
                if finish_reason == "content_filter" or is_refusal(generated_text):
                    refusal_attempt += 1
                    
                    # Log für diesen Refusal-Versuch
                    duration = (datetime.now() - start_time).total_seconds() * 1000
                    log_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "model": "gpt-4o",
                        "prompt_in": current_prompt,
                        "prompt_out": generated_text,
                        "error": f"Refusal detected (attempt {refusal_attempt}/{max_refusal_retries+1})",
                        "success": False,
                        "duration_ms": int(duration),
                        "retry_count": retry_count,
                        "refusal_attempts": refusal_attempt,
                        "quality_score": quality,
                        "cost": cost_info,
                        "style": style,
            "category": category
                    }
                    log_request(log_entry)
                    
                    if refusal_attempt <= max_refusal_retries:
                        # Neuen Prompt generieren (Variation)
                        current_prompt = f"{prompt} (Versuch {refusal_attempt + 1}: Formuliere es anders)"
                        print(f"  🔄 Refusal erkannt - Neuer Versuch {refusal_attempt + 1}/{max_refusal_retries + 1}")
                        time.sleep(1)
                        break  # Raus aus Inner Loop
                    else:
                        # Alle Refusal-Versuche aufgebraucht
                        result = {
                            "success": False,
                            "prompt_sent": original_prompt,
                            "prompt_generated": generated_text,
                            "error": f"Content refused after {refusal_attempt} attempts",
                            "model": "gpt-4o",
                            "duration_ms": int((datetime.now() - overall_start).total_seconds() * 1000),
                            "retries": retry_count,
                            "refusal_attempts": refusal_attempt,
                            "quality_score": quality,
                            "cost": cost_info,
                            "style": style,
            "category": category
                        }
                        return result
                else:
                    # Erfolg!
                    result = {
                        "success": True,
                        "prompt_sent": original_prompt,
                        "prompt_generated": generated_text,
                        "error": None,
                        "model": "gpt-4o",
                        "duration_ms": int((datetime.now() - overall_start).total_seconds() * 1000),
                        "retries": retry_count,
                        "refusal_attempts": refusal_attempt,
                        "quality_score": quality,
                        "cost": cost_info,
                        "style": style,
            "category": category
                    }
                    
                    # Final Log
                    log_entry = {
                        "timestamp": datetime.now().isoformat(),
                        **result,
                        "prompt_in": current_prompt,
                        "prompt_out": result["prompt_generated"],
                        "retry_count": result["retries"]
                    }
                    
                    log_request(log_entry)
                    return result
                    
            except RateLimitError as e:
                retry_count += 1
                if retry_count <= max_retries:
                    time.sleep(backoff_times[retry_count - 1])
                    continue
                else:
                    result = {
                        "success": False,
                        "prompt_sent": original_prompt,
                        "prompt_generated": None,
                        "error": f"Rate limit: {str(e)}",
                        "model": "gpt-4o",
                        "duration_ms": int((datetime.now() - overall_start).total_seconds() * 1000),
                        "retries": retry_count,
                        "refusal_attempts": refusal_attempt,
                        "quality_score": None,
                        "cost": None,
                        "style": style,
            "category": category
                    }
                    log_request({"timestamp": datetime.now().isoformat(), **result, "retry_count": retry_count})
                    return result
                    
            except (APIConnectionError, APITimeoutError) as e:
                retry_count += 1
                if retry_count <= max_retries:
                    time.sleep(backoff_times[retry_count - 1])
                    continue
                else:
                    result = {
                        "success": False,
                        "prompt_sent": original_prompt,
                        "prompt_generated": None,
                        "error": f"Connection error: {str(e)}",
                        "model": "gpt-4o",
                        "duration_ms": int((datetime.now() - overall_start).total_seconds() * 1000),
                        "retries": retry_count,
                        "refusal_attempts": refusal_attempt,
                        "quality_score": None,
                        "cost": None,
                        "style": style,
            "category": category
                    }
                    log_request({"timestamp": datetime.now().isoformat(), **result, "retry_count": retry_count})
                    return result
                    
            except Exception as e:
                result = {
                    "success": False,
                    "prompt_sent": original_prompt,
                    "prompt_generated": None,
                    "error": f"Error: {str(e)}",
                    "model": "gpt-4o",
                    "duration_ms": int((datetime.now() - overall_start).total_seconds() * 1000),
                    "retries": retry_count,
                    "refusal_attempts": refusal_attempt,
                    "quality_score": None,
                    "cost": None,
                    "style": style,
            "category": category
                }
                log_request({"timestamp": datetime.now().isoformat(), **result, "retry_count": retry_count})
                return result


if __name__ == "__main__":
    # Test
    result = generate_prompt("Künstliche Intelligenz", style="kreativ", max_tokens=200)
    print(json.dumps(result, indent=2, ensure_ascii=False))
