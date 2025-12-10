"""
SYNTX Prompts API
Clean flows. No patches. Field-based thinking.
"""
from fastapi import APIRouter, Query, HTTPException
from pathlib import Path
import json
from typing import Optional, Dict, List
from datetime import datetime
from collections import defaultdict, Counter

router = APIRouter(prefix="/prompts", tags=["prompts"])

QUEUE_DIR = Path("/opt/syntx-workflow-api-get-prompts/queue")
LOGS_DIR = Path("/opt/syntx-workflow-api-get-prompts/logs")

# ============================================================================
# CORE HELPERS - THE FOUNDATION
# ============================================================================

def load_all_processed() -> List[Dict]:
    """Load all processed prompts - SAFE"""
    processed = []
    processed_dir = QUEUE_DIR / "processed"
    
    if not processed_dir.exists():
        return processed
    
    for file in processed_dir.glob("*.json"):
        try:
            with open(file) as f:
                data = json.load(f)
                if data and isinstance(data, dict):
                    processed.append(data)
        except:
            continue
    
    return processed

def safe_get_score(prompt: dict) -> float:
    """Extract score - SAFE"""
    try:
        result = prompt.get('syntex_result')
        if not result or not isinstance(result, dict):
            return 0.0
        
        quality = result.get('quality_score')
        if not quality or not isinstance(quality, dict):
            return 0.0
        
        score = quality.get('total_score', 0)
        return float(score) if score else 0.0
    except:
        return 0.0

def safe_get_fields(prompt: dict) -> Dict[str, bool]:
    """Extract field breakdown - SAFE"""
    try:
        result = prompt.get('syntex_result')
        if not result or not isinstance(result, dict):
            return {}
        
        quality = result.get('quality_score')
        if not quality or not isinstance(quality, dict):
            return {}
        
        breakdown = quality.get('detail_breakdown', {})
        return breakdown if isinstance(breakdown, dict) else {}
    except:
        return {}

# ============================================================================
# BASIC QUERIES
# ============================================================================

@router.get("/all")
async def get_all_prompts(limit: int = Query(100, le=500)):
    """Get all prompts metadata (no text)"""
    processed = load_all_processed()
    
    # Build clean metadata
    results = []
    for p in processed[:limit]:
        results.append({
            "id": p.get('filename', 'unknown'),
            "topic": p.get('topic', 'unknown'),
            "style": p.get('style', 'unknown'),
            "category": p.get('category', 'unknown'),
            "score": safe_get_score(p),
            "timestamp": p.get('processed_at', ''),
            "wrapper": p.get('syntex_result', {}).get('wrapper', 'unknown') if isinstance(p.get('syntex_result'), dict) else 'unknown'
        })
    
    return {
        "status": "ALL_PROMPTS",
        "total": len(results),
        "prompts": results
    }

@router.get("/by-job/{job_id}")
async def get_by_job(job_id: str):
    """Get specific job by ID"""
    processed = load_all_processed()
    
    for p in processed:
        if job_id in str(p.get('filename', '')):
            return {
                "status": "JOB_FOUND",
                "data": p
            }
    
    raise HTTPException(status_code=404, detail="Job not found")

@router.get("/best")
async def get_best_prompts(limit: int = Query(20, le=100)):
    """Best performing prompts"""
    processed = load_all_processed()
    
    # Sort by score
    sorted_prompts = sorted(processed, key=lambda p: safe_get_score(p), reverse=True)
    
    results = []
    for p in sorted_prompts[:limit]:
        results.append({
            "id": p.get('filename', 'unknown'),
            "topic": p.get('topic', 'unknown'),
            "score": safe_get_score(p),
            "fields": safe_get_fields(p),
            "timestamp": p.get('processed_at', '')
        })
    
    return {
        "status": "BEST_PROMPTS",
        "total": len(results),
        "prompts": results
    }

# ============================================================================
# ANALYTICS
# ============================================================================

@router.get("/fields/breakdown")
async def fields_breakdown():
    """Field completion analysis"""
    processed = load_all_processed()
    
    field_stats = {
        'drift': {'present': 0, 'absent': 0},
        'hintergrund_muster': {'present': 0, 'absent': 0},
        'druckfaktoren': {'present': 0, 'absent': 0},
        'tiefe': {'present': 0, 'absent': 0},
        'wirkung': {'present': 0, 'absent': 0},
        'klartext': {'present': 0, 'absent': 0}
    }
    
    for p in processed:
        fields = safe_get_fields(p)
        for field in field_stats.keys():
            if fields.get(field):
                field_stats[field]['present'] += 1
            else:
                field_stats[field]['absent'] += 1
    
    # Calculate rates
    for field, stats in field_stats.items():
        total = stats['present'] + stats['absent']
        stats['completion_rate'] = round(stats['present'] / total, 2) if total > 0 else 0
    
    return {
        "status": "FIELD_BREAKDOWN",
        "total_analyzed": len(processed),
        "fields": field_stats
    }

@router.get("/costs/total")
async def total_costs():
    """Total GPT costs"""
    processed = load_all_processed()
    
    total_cost = 0.0
    total_tokens = {"input": 0, "output": 0}
    
    for p in processed:
        cost_data = p.get('gpt_cost', {})
        if isinstance(cost_data, dict):
            total_cost += cost_data.get('total_cost', 0)
            total_tokens['input'] += cost_data.get('input_tokens', 0)
            total_tokens['output'] += cost_data.get('output_tokens', 0)
    
    return {
        "status": "COSTS_CALCULATED",
        "total_prompts": len(processed),
        "total_cost_usd": round(total_cost, 4),
        "total_tokens": total_tokens,
        "avg_cost_per_prompt": round(total_cost / len(processed), 4) if len(processed) > 0 else 0
    }

@router.get("/search")
async def search_prompts(q: str = Query(..., min_length=2)):
    """Search in prompts"""
    processed = load_all_processed()
    
    q_lower = q.lower()
    results = []
    
    for p in processed:
        # Search in topic, style, category
        searchable = f"{p.get('topic', '')} {p.get('style', '')} {p.get('category', '')}".lower()
        if q_lower in searchable:
            results.append({
                "id": p.get('filename', 'unknown'),
                "topic": p.get('topic', 'unknown'),
                "style": p.get('style', 'unknown'),
                "score": safe_get_score(p),
                "match": "metadata"
            })
    
    return {
        "status": "SEARCH_COMPLETE",
        "query": q,
        "total_results": len(results),
        "results": results
    }

# ============================================================================
# TABLE VIEW - OVERVIEW WITHOUT TEXT
# ============================================================================

@router.get("/table-view")
async def prompts_table_view(
    limit: int = Query(50, le=200),
    min_score: float = Query(0, ge=0, le=100),
    topic: Optional[str] = None
):
    """
    🔥 TABLE VIEW - Fast overview without full text
    Use /full-text/{id} to get complete prompt
    """
    
    processed = load_all_processed()
    
    # Filters
    if min_score > 0:
        processed = [p for p in processed if safe_get_score(p) >= min_score]
    
    if topic:
        processed = [p for p in processed if p.get('topic', '').lower() == topic.lower()]
    
    # Limit
    processed = processed[:limit]
    
    # Build table
    table = []
    for p in processed:
        # Get fields fulfilled
        fields = safe_get_fields(p)
        fields_fulfilled = [k for k, v in fields.items() if v]
        
        # Get wrapper safely
        wrapper = 'unknown'
        result = p.get('syntex_result')
        if result and isinstance(result, dict):
            wrapper = result.get('wrapper', 'unknown')
        
        # Get duration safely
        duration_ms = 0
        if result and isinstance(result, dict):
            duration_ms = result.get('duration_ms', 0)
        
        row = {
            "id": p.get('filename', 'unknown'),
            "timestamp": p.get('processed_at', ''),
            "topic": p.get('topic', 'unknown'),
            "style": p.get('style', 'unknown'),
            "category": p.get('category', 'unknown'),
            "score": safe_get_score(p),
            "fields_fulfilled": fields_fulfilled,
            "field_count": f"{len(fields_fulfilled)}/6",
            "duration_ms": duration_ms,
            "wrapper": wrapper
        }
        
        table.append(row)
    
    return {
        "status": "TABLE_VIEW_READY",
        "total_rows": len(table),
        "filters": {
            "min_score": min_score,
            "topic": topic,
            "limit": limit
        },
        "table": table
    }

# ============================================================================
# FULL TEXT - COMPLETE PROMPT DETAILS
# ============================================================================

@router.get("/full-text/{filename}")
async def get_full_prompt_text(filename: str):
    """
    📄 VOLLTEXT - Complete prompt & response for ONE file
    
    Use Case: User clicks row in table → loads details
    """
    
    # Find metadata file
    processed_file = QUEUE_DIR / "processed" / filename
    if not processed_file.exists() and not filename.endswith('.json'):
        processed_file = QUEUE_DIR / "processed" / f"{filename}.json"
    
    if not processed_file.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {filename}")
    
    # Load metadata
    with open(processed_file) as f:
        data = json.load(f)
    
    # Load prompt text file
    prompt_text = ""
    txt_filename = data.get('filename', '')
    if txt_filename:
        prompt_file = QUEUE_DIR / "processed" / txt_filename
        if prompt_file.exists():
            try:
                with open(prompt_file) as f:
                    prompt_text = f.read()
            except Exception as e:
                prompt_text = f"[Error reading file: {e}]"
        else:
            prompt_text = f"[Prompt file not found: {txt_filename}]"
    
    # Get response (if stored)
    response_text = "[Response not stored in metadata]"
    result = data.get('syntex_result')
    if result and isinstance(result, dict):
        response_text = result.get('response_text', response_text)
    
    return {
        "status": "FULL_TEXT_LOADED",
        "filename": filename,
        "topic": data.get('topic', 'unknown'),
        "style": data.get('style', 'unknown'),
        "category": data.get('category', 'unknown'),
        "score": safe_get_score(data),
        "timestamp": data.get('processed_at', ''),
        "prompt_full_text": prompt_text,
        "response_full_text": response_text,
        "fields_breakdown": safe_get_fields(data),
        "duration_ms": result.get('duration_ms', 0) if result and isinstance(result, dict) else 0,
        "wrapper": result.get('wrapper', 'unknown') if result and isinstance(result, dict) else 'unknown',
        "gpt_quality": data.get('gpt_quality', {}),
        "gpt_cost": data.get('gpt_cost', {})
    }


# ============================================================================
# COMPLETE EXPORT - ALLES MIT VOLLTEXT
# ============================================================================


# ============================================================================
# COMPLETE EXPORT - ALLES MIT VOLLTEXT + PAGINATION
# ============================================================================

def load_all_calibrations() -> Dict[str, Dict]:
    """Load all calibrations and index by timestamp for matching"""
    calibrations_file = LOGS_DIR / "syntex_calibrations.jsonl"
    calibrations = []
    
    if not calibrations_file.exists():
        return {}
    
    try:
        with open(calibrations_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get('response') and entry.get('timestamp'):
                        calibrations.append(entry)
                except:
                    continue
    except:
        pass
    
    return calibrations

def find_response_by_timestamp(processed_timestamp: str, calibrations: list) -> str:
    """Find calibration response by nearest timestamp match"""
    if not processed_timestamp or not calibrations:
        return "[No response available]"
    
    try:
        # Parse processed timestamp (format: 2025-12-06T00:26:05.595595)
        proc_dt = datetime.fromisoformat(processed_timestamp.replace('Z', '+00:00'))
        
        # Find nearest calibration by time
        best_match = None
        min_diff = float('inf')
        
        for cal in calibrations:
            try:
                # Parse calibration timestamp (format: 2025-12-10T00:19:55.093607Z)
                cal_dt = datetime.fromisoformat(cal['timestamp'].replace('Z', '+00:00'))
                diff = abs((proc_dt - cal_dt).total_seconds())
                
                # Only match if within 5 minutes (300 seconds)
                if diff < min_diff and diff < 300:
                    min_diff = diff
                    best_match = cal
            except:
                continue
        
        if best_match:
            return best_match.get('response', '[Response found but empty]')
        
        return "[No matching response found]"
    except Exception as e:
        return f"[Error matching: {e}]"


@router.get("/complete-export")
async def complete_export(
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    page_size: int = Query(50, ge=1, le=200, description="Items per page"),
    min_score: float = Query(0, description="Minimum score filter"),
    topic: Optional[str] = Query(None, description="Filter by topic"),
    wrapper: Optional[str] = Query(None, description="Filter by wrapper")
):
    """
    🔥 COMPLETE EXPORT - ALLES MIT VOLLTEXT + PAGINATION
    
    Returns:
    - Full prompt text (from .txt files)
    - Full response text (from syntex_calibrations.jsonl)
    - All SYNTEX fields breakdown
    - All quality scores
    - All metadata
    
    Pagination:
    - page: Which page (1, 2, 3, ...)
    - page_size: Items per page (max 200)
    
    Example:
    - /prompts/complete-export?page=1&page_size=50
    - /prompts/complete-export?page=2&page_size=50&min_score=80
    """
    
    # Load all data
    processed = load_all_processed()
    
    if not processed:
        return {"status": "NO_DATA"}
    
    # Filters
    if min_score > 0:
        processed = [p for p in processed if safe_get_score(p) >= min_score]
    
    if topic:
        processed = [p for p in processed if p.get('topic', '').lower() == topic.lower()]
    
    if wrapper:
        filtered = []
        for p in processed:
            result = p.get('syntex_result')
            if result and isinstance(result, dict):
                if result.get('wrapper', '').lower() == wrapper.lower():
                    filtered.append(p)
        processed = filtered
    
    # Calculate pagination
    total_items = len(processed)
    total_pages = (total_items + page_size - 1) // page_size  # Ceiling division
    
    # Validate page
    if page > total_pages and total_pages > 0:
        return {
            "status": "PAGE_OUT_OF_RANGE",
            "page": page,
            "total_pages": total_pages,
            "total_items": total_items
        }
    
    # Get page slice
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    page_items = processed[start_idx:end_idx]
    
    # Build complete export
    exports = []
    
    for p in page_items:
        # Load prompt text
        prompt_text = ""
        txt_filename = p.get('filename', '')
        if txt_filename:
            prompt_file = QUEUE_DIR / "processed" / txt_filename
            if prompt_file.exists():
                try:
                    with open(prompt_file) as f:
                        prompt_text = f.read()
                except:
                    prompt_text = "[Error reading prompt]"
        
        # Get response from _response.txt file (new format) or JSON (backfilled)
        response_text = '[Response not available]'
        
        # Try 1: Load from _response.txt file (NEW FORMAT)
        txt_filename = p.get('filename', '')
        if txt_filename:
            response_file = QUEUE_DIR / "processed" / txt_filename.replace('.txt', '_response.txt')
            if response_file.exists():
                try:
                    with open(response_file) as f:
                        response_text = f.read()
                except:
                    pass
        
        # Try 2: Fallback to JSON (BACKFILLED DATA)
        if response_text == '[Response not available]':
            result = p.get('syntex_result')
            if result and isinstance(result, dict):
                response_text = result.get('response_text', '[Response not stored]')
        
        # Get fields
        fields = safe_get_fields(p)
        
        # Get result safely
        result = p.get('syntex_result')
        if not result or not isinstance(result, dict):
            result = {}
        
        # Build export item
        export_item = {
            "id": p.get('filename', 'unknown'),
            "timestamp": p.get('processed_at', ''),
            
            # Prompt Data
            "prompt": {
                "text": prompt_text,
                "topic": p.get('topic', 'unknown'),
                "style": p.get('style', 'unknown'),
                "category": p.get('category', 'unknown'),
                "language": p.get('language', 'de')
            },
            
            # Response Data
            "response": {
                "text": response_text,
                "wrapper": result.get('wrapper', 'unknown'),
                "duration_ms": result.get('duration_ms', 0)
            },
            
            # Quality Assessment
            "quality": {
                "total_score": safe_get_score(p),
                "fields_fulfilled": [k for k, v in fields.items() if v],
                "fields_missing": [k for k, v in fields.items() if not v],
                "field_breakdown": fields,
                "completion_rate": f"{len([v for v in fields.values() if v])}/6"
            },
            
            # GPT Metadata
            "gpt_metadata": {
                "quality_assessment": p.get('gpt_quality', {}),
                "cost": p.get('gpt_cost', {})
            }
        }
        
        exports.append(export_item)
    
    return {
        "status": "COMPLETE_EXPORT",
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        },
        "filters": {
            "min_score": min_score,
            "topic": topic,
            "wrapper": wrapper
        },
        "exports": exports
    }

