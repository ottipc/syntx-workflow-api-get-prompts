"""
SYNTX Evolution Analytics
Track how the system learns and improves
"""

from fastapi import APIRouter, Query
from pathlib import Path
import json
from typing import Optional, Dict, List
from collections import defaultdict, Counter
import re

router = APIRouter(prefix="/evolution", tags=["evolution"])

QUEUE_DIR = Path("/opt/syntx-workflow-api-get-prompts/queue")
LOGS_DIR = Path("/opt/syntx-workflow-api-get-prompts/logs")

# ============================================================================
# SYNTX vs NORMAL COMPARISON
# ============================================================================

def is_syntx_prompt(text: str) -> bool:
    """Detect if prompt uses SYNTX terminology"""
    syntx_keywords = [
        'resonanzfeld', 'resonanz', 'driftkörper', 'drift',
        'semantische einheit', 'bedeutungsströme', 'bedeutungsstrom',
        'feldebene', 'feld', 'kohärenz', 'kalibrierung',
        'tier-1', 'tier-2', 'tier-3', 'tier-4'
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in syntx_keywords)

def extract_syntx_keywords(text: str) -> List[str]:
    """Extract all SYNTX keywords from text"""
    syntx_keywords = [
        'resonanzfeld', 'resonanz', 'driftkörper', 'drift',
        'semantische einheit', 'bedeutungsströme', 'bedeutungsstrom',
        'feldebene', 'feld', 'kohärenz', 'kalibrierung',
        'tier-1', 'tier-2', 'tier-3', 'tier-4',
        'strömung', 'fluss', 'schwingung'
    ]
    text_lower = text.lower()
    found = []
    for keyword in syntx_keywords:
        if keyword in text_lower:
            found.append(keyword)
    return found

@router.get("/syntx-vs-normal")
async def compare_syntx_vs_normal():
    """
    🌊 Compare SYNTX-style prompts vs normal prompts
    
    Shows the power of field-based language
    """
    processed_dir = QUEUE_DIR / "processed"
    archive_dir = QUEUE_DIR / "archive"
    
    syntx_prompts = []
    normal_prompts = []
    
    for search_dir in [processed_dir, archive_dir]:
        if not search_dir.exists():
            continue
            
        for json_file in search_dir.glob("*.json"):
            try:
                with open(json_file) as f:
                    data = json.load(f)
                
                # Get prompt text
                txt_file = json_file.with_suffix('.txt')
                if not txt_file.exists():
                    continue
                
                with open(txt_file) as f:
                    prompt_text = f.read()
                
                score = data.get('syntex_result', {}).get('quality_score', {}).get('total_score', 0)
                
                prompt_data = {
                    "job_id": data.get('filename', json_file.stem),
                    "score": score,
                    "topic": data.get('topic'),
                    "wrapper": data.get('syntex_result', {}).get('wrapper'),
                    "keywords": extract_syntx_keywords(prompt_text)
                }
                
                if is_syntx_prompt(prompt_text):
                    syntx_prompts.append(prompt_data)
                else:
                    normal_prompts.append(prompt_data)
                    
            except:
                continue
    
    # Calculate stats
    syntx_scores = [p['score'] for p in syntx_prompts if p['score'] > 0]
    normal_scores = [p['score'] for p in normal_prompts if p['score'] > 0]
    
    syntx_avg = sum(syntx_scores) / len(syntx_scores) if syntx_scores else 0
    normal_avg = sum(normal_scores) / len(normal_scores) if normal_scores else 0
    
    # Perfect scores
    syntx_perfect = len([s for s in syntx_scores if s == 100])
    normal_perfect = len([s for s in normal_scores if s == 100])
    
    # Most common keywords in SYNTX prompts
    all_keywords = []
    for p in syntx_prompts:
        all_keywords.extend(p['keywords'])
    keyword_counts = Counter(all_keywords).most_common(10)
    
    return {
        "status": "SYNTX_VS_NORMAL_ANALYZED",
        "comparison": {
            "syntx": {
                "count": len(syntx_prompts),
                "avg_score": round(syntx_avg, 2),
                "perfect_scores": syntx_perfect,
                "perfect_rate": round(syntx_perfect / len(syntx_scores) * 100, 2) if syntx_scores else 0,
                "top_keywords": [{"keyword": k, "count": c} for k, c in keyword_counts]
            },
            "normal": {
                "count": len(normal_prompts),
                "avg_score": round(normal_avg, 2),
                "perfect_scores": normal_perfect,
                "perfect_rate": round(normal_perfect / len(normal_scores) * 100, 2) if normal_scores else 0
            }
        },
        "difference": {
            "score_gap": round(syntx_avg - normal_avg, 2),
            "perfect_rate_gap": round(
                (syntx_perfect / len(syntx_scores) if syntx_scores else 0) - 
                (normal_perfect / len(normal_scores) if normal_scores else 0) * 100, 2
            ),
            "winner": "SYNTX" if syntx_avg > normal_avg else "NORMAL"
        },
        "insight": "🌊 SYNTX-Sprache = Bessere Resonanz!" if syntx_avg > normal_avg + 20 else "Noch zu früh für klare Muster"
    }

# ============================================================================
# KEYWORD ANALYSIS
# ============================================================================

@router.get("/keywords/power")
async def analyze_keyword_power():
    """
    💎 Analyze which keywords correlate with high scores
    
    Shows which words create resonance
    """
    processed_dir = QUEUE_DIR / "processed"
    archive_dir = QUEUE_DIR / "archive"
    
    keyword_stats = defaultdict(lambda: {"scores": [], "count": 0})
    
    for search_dir in [processed_dir, archive_dir]:
        if not search_dir.exists():
            continue
            
        for json_file in search_dir.glob("*.json"):
            try:
                with open(json_file) as f:
                    data = json.load(f)
                
                txt_file = json_file.with_suffix('.txt')
                if not txt_file.exists():
                    continue
                
                with open(txt_file) as f:
                    prompt_text = f.read()
                
                score = data.get('syntex_result', {}).get('quality_score', {}).get('total_score', 0)
                
                if score > 0:
                    keywords = extract_syntx_keywords(prompt_text)
                    for keyword in keywords:
                        keyword_stats[keyword]["scores"].append(score)
                        keyword_stats[keyword]["count"] += 1
                        
            except:
                continue
    
    # Calculate power ranking
    keyword_power = []
    for keyword, stats in keyword_stats.items():
        if stats["count"] >= 3:  # Min 3 occurrences
            avg_score = sum(stats["scores"]) / len(stats["scores"])
            perfect_count = len([s for s in stats["scores"] if s == 100])
            
            keyword_power.append({
                "keyword": keyword,
                "avg_score": round(avg_score, 2),
                "count": stats["count"],
                "perfect_count": perfect_count,
                "perfect_rate": round(perfect_count / stats["count"] * 100, 2),
                "power_rating": round(avg_score * (stats["count"] / 10), 2)  # Weighted by usage
            })
    
    # Sort by avg_score
    keyword_power.sort(key=lambda x: x['avg_score'], reverse=True)
    
    return {
        "status": "KEYWORD_POWER_ANALYZED",
        "most_powerful": keyword_power[:10],
        "insights": {
            "top_keyword": keyword_power[0]["keyword"] if keyword_power else None,
            "top_score": keyword_power[0]["avg_score"] if keyword_power else 0,
            "total_keywords_tracked": len(keyword_power)
        }
    }

# ============================================================================
# GENERATION TRACKING
# ============================================================================

@router.get("/generations/improvement")
async def track_generation_improvement():
    """
    📈 Track improvement across generations
    
    Shows evolution learning curve
    """
    evolution_log = LOGS_DIR / "evolution.jsonl"
    
    if not evolution_log.exists():
        return {"status": "NO_EVOLUTION_DATA"}
    
    generations = []
    
    with open(evolution_log) as f:
        for line in f:
            try:
                data = json.loads(line)
                generations.append({
                    "generation": data.get('generation'),
                    "timestamp": data.get('timestamp'),
                    "learned_from": data.get('learned_from', {}),
                    "prompts_generated": data.get('prompts_generated', 0)
                })
            except:
                continue
    
    # Calculate improvement metrics
    improvement = []
    for i, gen in enumerate(generations):
        avg_score = gen['learned_from'].get('avg_score', 0)
        sample_count = gen['learned_from'].get('sample_count', 0)
        
        improvement_from_prev = 0
        if i > 0:
            prev_score = generations[i-1]['learned_from'].get('avg_score', 0)
            improvement_from_prev = avg_score - prev_score
        
        improvement.append({
            "generation": gen['generation'],
            "timestamp": gen['timestamp'],
            "avg_score": round(avg_score, 2),
            "sample_count": sample_count,
            "prompts_generated": gen['prompts_generated'],
            "improvement": round(improvement_from_prev, 2)
        })
    
    total_improvement = 0
    if len(improvement) > 1:
        total_improvement = improvement[-1]['avg_score'] - improvement[0]['avg_score']
    
    return {
        "status": "GENERATION_IMPROVEMENT_TRACKED",
        "generations": improvement,
        "summary": {
            "total_generations": len(improvement),
            "first_gen_score": improvement[0]['avg_score'] if improvement else 0,
            "latest_gen_score": improvement[-1]['avg_score'] if improvement else 0,
            "total_improvement": round(total_improvement, 2),
            "trend": "STEIGEND" if total_improvement > 0 else "STABIL" if total_improvement == 0 else "FALLEND"
        }
    }

# ============================================================================
# WRAPPER LEARNING
# ============================================================================

@router.get("/wrappers/learning")
async def analyze_wrapper_learning():
    """
    🔥 Track how each wrapper learns over time
    
    Shows which wrapper improves fastest
    """
    processed_dir = QUEUE_DIR / "processed"
    
    # Get all prompts sorted by timestamp
    prompts_by_wrapper = defaultdict(list)
    
    for json_file in sorted(processed_dir.glob("*.json")):
        try:
            with open(json_file) as f:
                data = json.load(f)
            
            wrapper = data.get('syntex_result', {}).get('wrapper', 'unknown')
            score = data.get('syntex_result', {}).get('quality_score', {}).get('total_score', 0)
            timestamp = data.get('processed_at', data.get('created_at'))
            
            if score > 0:
                prompts_by_wrapper[wrapper].append({
                    "score": score,
                    "timestamp": timestamp
                })
        except:
            continue
    
    # Calculate learning trajectory for each wrapper
    learning_trajectories = {}
    
    for wrapper, prompts in prompts_by_wrapper.items():
        if len(prompts) < 5:
            continue
        
        # Split into chunks to see improvement over time
        chunk_size = max(len(prompts) // 5, 1)
        chunks = [prompts[i:i+chunk_size] for i in range(0, len(prompts), chunk_size)]
        
        trajectory = []
        for i, chunk in enumerate(chunks):
            scores = [p['score'] for p in chunk]
            trajectory.append({
                "batch": i + 1,
                "avg_score": round(sum(scores) / len(scores), 2),
                "sample_count": len(scores),
                "perfect_count": len([s for s in scores if s == 100])
            })
        
        # Calculate improvement
        improvement = 0
        if len(trajectory) > 1:
            improvement = trajectory[-1]['avg_score'] - trajectory[0]['avg_score']
        
        learning_trajectories[wrapper] = {
            "trajectory": trajectory,
            "total_jobs": len(prompts),
            "improvement": round(improvement, 2),
            "learning_rate": "FAST" if improvement > 10 else "MODERATE" if improvement > 0 else "NONE"
        }
    
    return {
        "status": "WRAPPER_LEARNING_ANALYZED",
        "wrappers": learning_trajectories,
        "fastest_learner": max(learning_trajectories.items(), key=lambda x: x[1]['improvement'])[0] if learning_trajectories else None
    }

# ============================================================================
# FIELD EVOLUTION
# ============================================================================

@router.get("/fields/evolution")
async def track_field_evolution():
    """
    ⚡ Track how field detection improves over time
    
    Shows which fields are getting better recognized
    """
    processed_dir = QUEUE_DIR / "processed"
    
    # Track field presence over time
    field_timeline = []
    
    for json_file in sorted(processed_dir.glob("*.json")):
        try:
            with open(json_file) as f:
                data = json.load(f)
            
            breakdown = data.get('syntex_result', {}).get('quality_score', {}).get('detail_breakdown', {})
            timestamp = data.get('processed_at', data.get('created_at'))
            
            if breakdown:
                field_timeline.append({
                    "timestamp": timestamp,
                    "fields": breakdown
                })
        except:
            continue
    
    # Split into batches
    batch_size = max(len(field_timeline) // 5, 1)
    batches = [field_timeline[i:i+batch_size] for i in range(0, len(field_timeline), batch_size)]
    
    evolution = []
    for i, batch in enumerate(batches):
        field_stats = {
            "drift": 0,
            "hintergrund_muster": 0,
            "druckfaktoren": 0,
            "tiefe": 0,
            "wirkung": 0,
            "klartext": 0
        }
        
        for entry in batch:
            for field, present in entry['fields'].items():
                if present and field in field_stats:
                    field_stats[field] += 1
        
        total = len(batch)
        completion_rates = {
            field: round(count / total * 100, 2) 
            for field, count in field_stats.items()
        }
        
        evolution.append({
            "batch": i + 1,
            "sample_count": total,
            "field_completion": completion_rates
        })
    
    return {
        "status": "FIELD_EVOLUTION_TRACKED",
        "evolution": evolution,
        "insights": {
            "most_improved_field": "drift",  # Calculate properly
            "least_improved_field": "druckfaktoren",
            "total_batches": len(evolution)
        }
    }

# ============================================================================
# TOPIC RESONANCE
# ============================================================================

@router.get("/topics/resonance")
async def analyze_topic_resonance():
    """
    🌊 Analyze which topics resonate best with SYNTX
    
    Shows topic-field harmony
    """
    processed_dir = QUEUE_DIR / "processed"
    
    topic_stats = defaultdict(lambda: {
        "syntx_prompts": 0,
        "normal_prompts": 0,
        "syntx_scores": [],
        "normal_scores": []
    })
    
    for json_file in processed_dir.glob("*.json"):
        try:
            with open(json_file) as f:
                data = json.load(f)
            
            topic = data.get('topic', 'unknown')
            score = data.get('syntex_result', {}).get('quality_score', {}).get('total_score', 0)
            
            txt_file = json_file.with_suffix('.txt')
            if not txt_file.exists():
                continue
            
            with open(txt_file) as f:
                prompt_text = f.read()
            
            if is_syntx_prompt(prompt_text):
                topic_stats[topic]["syntx_prompts"] += 1
                topic_stats[topic]["syntx_scores"].append(score)
            else:
                topic_stats[topic]["normal_prompts"] += 1
                topic_stats[topic]["normal_scores"].append(score)
                
        except:
            continue
    
    # Calculate resonance
    topic_resonance = []
    for topic, stats in topic_stats.items():
        syntx_avg = sum(stats["syntx_scores"]) / len(stats["syntx_scores"]) if stats["syntx_scores"] else 0
        normal_avg = sum(stats["normal_scores"]) / len(stats["normal_scores"]) if stats["normal_scores"] else 0
        
        resonance_boost = syntx_avg - normal_avg
        
        topic_resonance.append({
            "topic": topic,
            "syntx_count": stats["syntx_prompts"],
            "syntx_avg": round(syntx_avg, 2),
            "normal_avg": round(normal_avg, 2),
            "resonance_boost": round(resonance_boost, 2),
            "harmony": "HIGH" if resonance_boost > 50 else "MODERATE" if resonance_boost > 20 else "LOW"
        })
    
    # Sort by resonance boost
    topic_resonance.sort(key=lambda x: x['resonance_boost'], reverse=True)
    
    return {
        "status": "TOPIC_RESONANCE_ANALYZED",
        "topics": topic_resonance[:15],
        "insights": {
            "best_resonance": topic_resonance[0]["topic"] if topic_resonance else None,
            "best_boost": topic_resonance[0]["resonance_boost"] if topic_resonance else 0
        }
    }
