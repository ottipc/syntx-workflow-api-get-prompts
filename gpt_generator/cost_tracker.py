"""
OpenAI API Cost Tracking
Berechnet und tracked Kosten für API-Calls
"""
import json
from pathlib import Path
from datetime import datetime


# OpenAI Pricing (Stand Nov 2025, in USD)
PRICING = {
    "gpt-4o": {
        "input": 2.50 / 1_000_000,   # $2.50 per 1M input tokens
        "output": 10.00 / 1_000_000   # $10.00 per 1M output tokens
    }
}


def calculate_cost(usage: dict, model: str = "gpt-4o") -> dict:
    """
    Berechnet die Kosten eines API-Calls.
    
    Args:
        usage: Dict mit prompt_tokens und completion_tokens
        model: Model-Name (default: gpt-4o)
        
    Returns:
        dict mit detaillierten Kosten
    """
    if model not in PRICING:
        return {
            "input_cost": 0.0,
            "output_cost": 0.0,
            "total_cost": 0.0,
            "currency": "USD"
        }
    
    input_tokens = usage.get("prompt_tokens", 0)
    output_tokens = usage.get("completion_tokens", 0)
    
    input_cost = input_tokens * PRICING[model]["input"]
    output_cost = output_tokens * PRICING[model]["output"]
    total_cost = input_cost + output_cost
    
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_cost": round(input_cost, 6),
        "output_cost": round(output_cost, 6),
        "total_cost": round(total_cost, 6),
        "currency": "USD"
    }


def save_cost_log(cost_data: dict) -> None:
    """Speichert Cost-Log in separate Datei."""
    log_dir = Path("./logs")
    log_dir.mkdir(exist_ok=True)
    
    cost_file = log_dir / "costs.jsonl"
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        **cost_data
    }
    
    with open(cost_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")


def get_total_costs(days: int = None) -> dict:
    """
    Berechnet Gesamt-Kosten aus Cost-Logs.
    
    Args:
        days: Nur Kosten der letzten N Tage (None = alle)
        
    Returns:
        dict mit Gesamt-Statistiken
    """
    log_dir = Path("./logs")
    cost_file = log_dir / "costs.jsonl"
    
    if not cost_file.exists():
        return {
            "total_cost": 0.0,
            "total_requests": 0,
            "avg_cost_per_request": 0.0,
            "currency": "USD"
        }
    
    total_cost = 0.0
    total_requests = 0
    
    with open(cost_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                total_cost += entry.get("total_cost", 0.0)
                total_requests += 1
            except:
                continue
    
    avg_cost = total_cost / total_requests if total_requests > 0 else 0.0
    
    return {
        "total_cost": round(total_cost, 4),
        "total_requests": total_requests,
        "avg_cost_per_request": round(avg_cost, 6),
        "currency": "USD"
    }


if __name__ == "__main__":
    # Test
    test_usage = {
        "prompt_tokens": 50,
        "completion_tokens": 200
    }
    
    cost = calculate_cost(test_usage, "gpt-4o")
    print(f"Cost Calculation Test:")
    print(f"  Input: {cost['input_tokens']} tokens = ${cost['input_cost']}")
    print(f"  Output: {cost['output_tokens']} tokens = ${cost['output_cost']}")
    print(f"  Total: ${cost['total_cost']}")
    
    # Test save
    save_cost_log(cost)
    print(f"\n✅ Cost logged to ./logs/costs.jsonl")
    
    # Test total
    stats = get_total_costs()
    print(f"\nTotal Stats:")
    print(f"  Total Cost: ${stats['total_cost']}")
    print(f"  Total Requests: {stats['total_requests']}")
    print(f"  Avg per Request: ${stats['avg_cost_per_request']}")
