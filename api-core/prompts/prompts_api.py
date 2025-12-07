"""
SYNTX Prompts & Results API
Full access to generated prompts and their evaluations
"""

from fastapi import APIRouter, Query, HTTPException
from pathlib import Path
import json
from typing import Optional, List, Dict
from datetime import datetime

router = APIRouter(prefix="/prompts", tags=["prompts"])

QUEUE_DIR = Path("/opt/syntx-workflow-api-get-prompts/queue")
LOGS_DIR = Path("/opt/syntx-workflow-api-get-prompts/logs")

# ============================================================================
# PROMPTS & RESULTS
# ============================================================================

@router.get("/all")
async def get_all_prompts(
    limit: int = Query(50, le=200),
    topic: Optional[str] = None,
    style: Optional[str] = None,
    category: Optional[str] = None,
    min_score: Optional[int] = None,
    wrapper: Optional[str] = None
):
    """
    Get all processed prompts with full details
    
    Returns: Prompt text, GPT quality, SYNTEX scores, costs
    """
    processed_dir = QUEUE_DIR / "processed"
    
    if not processed_dir.exists():
        return {"status": "NO_DATA", "prompts": []}
    
    prompts = []
    
    for json_file in sorted(processed_dir.glob("*.json"), reverse=True):
        try:
            with open(json_file) as f:
                data = json.load(f)
            
            # Apply filters
            if topic and data.get('topic', '').lower() != topic.lower():
                continue
            if style and data.get('style', '').lower() != style.lower():
                continue
            if category and data.get('category', '').lower() != category.lower():
                continue
            if wrapper and data.get('syntex_result', {}).get('wrapper', '').lower() != wrapper.lower():
                continue
            
            # Score filter
            syntex_score = data.get('syntex_result', {}).get('quality_score', {}).get('total_score', 0)
            if min_score and syntex_score < min_score:
                continue
            
            # Get prompt text
            txt_file = json_file.parent.parent / "archive" / json_file.name.replace('.json', '.txt')
            if not txt_file.exists():
                # Try in processed directly
                txt_file = json_file.with_suffix('.txt')
            
            prompt_text = ""
            if txt_file.exists():
                with open(txt_file) as f:
                    prompt_text = f.read()
            
            prompts.append({
                "job_id": data.get('filename', json_file.stem),
                "topic": data.get('topic'),
                "style": data.get('style'),
                "category": data.get('category'),
                "prompt_text": prompt_text,
                "gpt_quality": data.get('gpt_quality'),
                "syntex_result": data.get('syntex_result'),
                "costs": data.get('gpt_cost'),
                "created_at": data.get('created_at'),
                "processed_at": data.get('processed_at')
            })
            
            if len(prompts) >= limit:
                break
                
        except Exception as e:
            continue
    
    return {
        "status": "PROMPTS_RETRIEVED",
        "count": len(prompts),
        "prompts": prompts
    }

@router.get("/by-job/{job_id}")
async def get_prompt_by_id(job_id: str):
    """Get specific prompt by job ID"""
    processed_dir = QUEUE_DIR / "processed"
    archive_dir = QUEUE_DIR / "archive"
    
    # Try to find the file
    for search_dir in [processed_dir, archive_dir]:
        matches = list(search_dir.glob(f"*{job_id}*.json"))
        if matches:
            json_file = matches[0]
            break
    else:
        raise HTTPException(404, "Job not found")
    
    with open(json_file) as f:
        data = json.load(f)
    
    # Get prompt text
    txt_file = json_file.with_suffix('.txt')
    prompt_text = ""
    if txt_file.exists():
        with open(txt_file) as f:
            prompt_text = f.read()
    
    return {
        "status": "PROMPT_FOUND",
        "job_id": job_id,
        "data": {
            "topic": data.get('topic'),
            "style": data.get('style'),
            "category": data.get('category'),
            "prompt_text": prompt_text,
            "gpt_quality": data.get('gpt_quality'),
            "syntex_result": data.get('syntex_result'),
            "costs": data.get('gpt_cost'),
            "created_at": data.get('created_at'),
            "processed_at": data.get('processed_at')
        }
    }

@router.get("/best")
async def get_best_prompts(limit: int = Query(20, le=100)):
    """Get best performing prompts"""
    processed_dir = QUEUE_DIR / "processed"
    
    prompts_with_scores = []
    
    for json_file in processed_dir.glob("*.json"):
        try:
            with open(json_file) as f:
                data = json.load(f)
            
            syntex_score = data.get('syntex_result', {}).get('quality_score', {}).get('total_score', 0)
            
            if syntex_score > 0:
                prompts_with_scores.append({
                    "job_id": data.get('filename', json_file.stem),
                    "topic": data.get('topic'),
                    "style": data.get('style'),
                    "wrapper": data.get('syntex_result', {}).get('wrapper'),
                    "score": syntex_score,
                    "gpt_quality": data.get('gpt_quality', {}).get('total_score', 0)
                })
        except:
            continue
    
    prompts_with_scores.sort(key=lambda x: x['score'], reverse=True)
    
    return {
        "status": "BEST_PROMPTS",
        "count": len(prompts_with_scores[:limit]),
        "prompts": prompts_with_scores[:limit]
    }

@router.get("/fields/breakdown")
async def get_field_breakdown(
    topic: Optional[str] = None,
    wrapper: Optional[str] = None
):
    """Analyze SYNTEX field completeness"""
    processed_dir = QUEUE_DIR / "processed"
    
    field_stats = {
        "drift": {"present": 0, "absent": 0},
        "hintergrund_muster": {"present": 0, "absent": 0},
        "druckfaktoren": {"present": 0, "absent": 0},
        "tiefe": {"present": 0, "absent": 0},
        "wirkung": {"present": 0, "absent": 0},
        "klartext": {"present": 0, "absent": 0}
    }
    
    total = 0
    
    for json_file in processed_dir.glob("*.json"):
        try:
            with open(json_file) as f:
                data = json.load(f)
            
            if topic and data.get('topic', '').lower() != topic.lower():
                continue
            if wrapper and data.get('syntex_result', {}).get('wrapper', '').lower() != wrapper.lower():
                continue
            
            breakdown = data.get('syntex_result', {}).get('quality_score', {}).get('detail_breakdown', {})
            
            for field, present in breakdown.items():
                if field in field_stats:
                    if present:
                        field_stats[field]["present"] += 1
                    else:
                        field_stats[field]["absent"] += 1
            
            total += 1
        except:
            continue
    
    field_completion = {}
    for field, stats in field_stats.items():
        if stats["present"] + stats["absent"] > 0:
            completion = stats["present"] / (stats["present"] + stats["absent"]) * 100
            field_completion[field] = {
                "completion_rate": round(completion, 2),
                "present": stats["present"],
                "absent": stats["absent"]
            }
    
    return {
        "status": "FIELD_BREAKDOWN",
        "total_analyzed": total,
        "fields": field_completion
    }

@router.get("/costs/total")
async def get_total_costs():
    """Calculate total GPT-4 costs"""
    costs_log = LOGS_DIR / "costs.jsonl"
    
    total_cost = 0
    total_input_tokens = 0
    total_output_tokens = 0
    count = 0
    
    if costs_log.exists():
        with open(costs_log) as f:
            for line in f:
                try:
                    data = json.loads(line)
                    total_cost += data.get('total_cost', 0)
                    total_input_tokens += data.get('input_tokens', 0)
                    total_output_tokens += data.get('output_tokens', 0)
                    count += 1
                except:
                    continue
    
    return {
        "status": "COSTS_CALCULATED",
        "total_prompts": count,
        "total_cost_usd": round(total_cost, 4),
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "avg_cost_per_prompt": round(total_cost / count, 6) if count > 0 else 0
    }

@router.get("/search")
async def search_prompts(
    q: str = Query(..., min_length=3),
    limit: int = Query(20, le=100)
):
    """Search prompts by text content"""
    processed_dir = QUEUE_DIR / "processed"
    archive_dir = QUEUE_DIR / "archive"
    
    results = []
    q_lower = q.lower()
    
    for txt_file in list(processed_dir.glob("*.txt")) + list(archive_dir.glob("*.txt")):
        try:
            with open(txt_file) as f:
                content = f.read()
            
            if q_lower in content.lower():
                json_file = txt_file.with_suffix('.json')
                if json_file.exists():
                    with open(json_file) as f:
                        data = json.load(f)
                    
                    results.append({
                        "job_id": data.get('filename', txt_file.stem),
                        "topic": data.get('topic'),
                        "style": data.get('style'),
                        "score": data.get('syntex_result', {}).get('quality_score', {}).get('total_score', 0),
                        "snippet": content[:200] + "..." if len(content) > 200 else content
                    })
            
            if len(results) >= limit:
                break
                
        except:
            continue
    
    return {
        "status": "SEARCH_COMPLETE",
        "query": q,
        "count": len(results),
        "results": results
    }
