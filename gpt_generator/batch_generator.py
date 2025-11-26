"""
Batch Prompt Generator
Generiert mehrere Prompts auf einmal mit verschiedenen Topics und Styles
"""
import json
import random
from datetime import datetime
from gpt_generator.syntx_prompt_generator import generate_prompt
from gpt_generator.topics_database import get_random_topics
from prompt_styles import get_all_styles
from cost_tracker import get_total_costs


def generate_batch(count: int = 20, use_random_styles: bool = True) -> dict:
    """
    Generiert mehrere Prompts auf einmal.
    
    Args:
        count: Anzahl zu generierender Prompts
        use_random_styles: Ob zufällige Styles verwendet werden sollen
        
    Returns:
        dict mit Ergebnissen und Statistiken
    """
    
    print(f"\n{'='*80}")
    print(f"BATCH GENERATION - {count} Prompts")
    print(f"{'='*80}\n")
    
    # Zufällige Topics holen
    topics = get_random_topics(count)
    styles = get_all_styles()
    
    results = []
    stats = {
        "total": count,
        "successful": 0,
        "refused": 0,
        "errors": 0,
        "by_category": {},
        "by_style": {},
        "total_cost": 0.0,
        "avg_quality": 0.0
    }
    
    for i, (category, topic) in enumerate(topics, 1):
        # Zufälligen Style wählen
        style = random.choice(styles) if use_random_styles else "technisch"
        
        print(f"[{i}/{count}] {category.upper()}: {topic}")
        print(f"        Style: {style}")
        
        # Prompt generieren
        result = generate_prompt(
            topic,
            style=style,
            max_tokens=400,
            max_refusal_retries=3,
            category=category
        )
        
        results.append({
            "category": category,
            "topic": topic,
            "style": style,
            "result": result,
            "category": category
            })
        
        # Statistiken updaten
        if category not in stats["by_category"]:
            stats["by_category"][category] = {"total": 0, "success": 0, "refused": 0}
        stats["by_category"][category]["total"] += 1
        
        if style not in stats["by_style"]:
            stats["by_style"][style] = {"total": 0, "success": 0}
        stats["by_style"][style]["total"] += 1
        
        if result["success"]:
            stats["successful"] += 1
            stats["by_category"][category]["success"] += 1
            stats["by_style"][style]["success"] += 1
            
            if result.get("cost"):
                stats["total_cost"] += result["cost"]["total_cost"]
            
            if result.get("quality_score"):
                stats["avg_quality"] += result["quality_score"]["total_score"]
            
            quality_info = ""
            if result.get("quality_score"):
                quality_info = f" | ⭐ {result['quality_score']['total_score']}/10"
            
            cost_info = ""
            if result.get("cost"):
                cost_info = f" | 💰 ${result['cost']['total_cost']}"
            
            print(f"        ✅ OK ({result['duration_ms']}ms{quality_info}{cost_info})")
        else:
            if "refused" in result.get("error", "").lower():
                stats["refused"] += 1
                stats["by_category"][category]["refused"] += 1
                print(f"        🚫 REFUSED")
            else:
                stats["errors"] += 1
                print(f"        ❌ ERROR: {result.get('error', 'Unknown')}")
        
        print()
    
    # Durchschnitte berechnen
    if stats["successful"] > 0:
        stats["avg_quality"] = round(stats["avg_quality"] / stats["successful"], 2)
    
    # Zusammenfassung
    print(f"\n{'='*80}")
    print("ZUSAMMENFASSUNG")
    print(f"{'='*80}")
    print(f"Total:         {stats['total']}")
    print(f"✅ Erfolg:     {stats['successful']} ({stats['successful']/stats['total']*100:.1f}%)")
    print(f"🚫 Refused:    {stats['refused']} ({stats['refused']/stats['total']*100:.1f}%)")
    print(f"❌ Errors:     {stats['errors']} ({stats['errors']/stats['total']*100:.1f}%)")
    print(f"💰 Total Cost: ${stats['total_cost']:.4f}")
    print(f"⭐ Avg Quality: {stats['avg_quality']}/10")
    
    print(f"\n{'='*80}")
    print("NACH KATEGORIE")
    print(f"{'='*80}")
    for cat, cat_stats in sorted(stats["by_category"].items()):
        success_rate = cat_stats["success"]/cat_stats["total"]*100 if cat_stats["total"] > 0 else 0
        print(f"{cat:15} | Total: {cat_stats['total']:2} | ✅ {cat_stats['success']:2} | 🚫 {cat_stats['refused']:2} | Success: {success_rate:5.1f}%")
    
    print(f"\n{'='*80}")
    print("NACH STYLE")
    print(f"{'='*80}")
    for style, style_stats in sorted(stats["by_style"].items()):
        success_rate = style_stats["success"]/style_stats["total"]*100 if style_stats["total"] > 0 else 0
        print(f"{style:15} | Total: {style_stats['total']:2} | ✅ {style_stats['success']:2} | Success: {success_rate:5.1f}%")
    
    # Gesamtkosten (lifetime)
    lifetime_costs = get_total_costs()
    print(f"\n{'='*80}")
    print("LIFETIME COSTS")
    print(f"{'='*80}")
    print(f"Total Requests: {lifetime_costs['total_requests']}")
    print(f"Total Cost: ${lifetime_costs['total_cost']}")
    print(f"Avg per Request: ${lifetime_costs['avg_cost_per_request']}")
    
    return {
        "results": results,
        "stats": stats,
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    # Generiere 20 Prompts
    batch_result = generate_batch(count=20, use_random_styles=True)
    
    # Optional: Speichere Batch-Ergebnis
    # with open(f"./logs/batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
    #     json.dump(batch_result, f, ensure_ascii=False, indent=2)
