"""
SYNTX Advanced Prompts API
Features: Predict, Analysis, Templates
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
from pathlib import Path
import re

router = APIRouter(prefix="/prompts/advanced", tags=["prompts-advanced"])

# Base paths
QUEUE_DIR = Path("/opt/syntx-workflow-api-get-prompts/queue")
PROCESSED_DIR = QUEUE_DIR / "processed"


# === MODELS ===

class PredictRequest(BaseModel):
    prompt_text: str
    topic: str
    style: str
    wrapper: Optional[str] = "syntex_system"


# === HELPER: Load all processed for analysis ===

def load_all_processed():
    """Load all processed jobs with safe error handling"""
    processed = []
    
    for json_file in PROCESSED_DIR.glob("*.json"):
        try:
            with open(json_file) as f:
                data = json.load(f)
                processed.append(data)
        except:
            continue
    
    return processed


# === HELPER: Extract keywords ===

def extract_keywords(text: str) -> dict:
    """Extract SYNTX keywords from text"""
    text_lower = text.lower()
    
    keywords = {
        # TIER keywords
        'tier': len(re.findall(r'tier-[1234]', text_lower)),
        
        # Field keywords
        'drift': text_lower.count('drift'),
        'driftkörper': text_lower.count('driftkörper'),
        'kalibrierung': text_lower.count('kalibrierung'),
        'strömung': text_lower.count('strömung'),
        'stromung': text_lower.count('stromung'),
        'resonanz': text_lower.count('resonanz'),
        'feld': text_lower.count('feld'),
        
        # Meta keywords
        'system': text_lower.count('system'),
        'mechanismus': text_lower.count('mechanismus'),
        'struktur': text_lower.count('struktur'),
    }
    
    return keywords


# === HELPER: Calculate keyword score ===

def calculate_keyword_score(keywords: dict) -> float:
    """Calculate score based on keyword presence"""
    score = 50.0  # Base score
    
    # TIER keywords (strongest!)
    if keywords['tier'] > 0:
        score += min(keywords['tier'] * 15, 30)  # Max +30
    
    # Core SYNTX keywords
    if keywords['driftkörper'] > 0:
        score += 10
    if keywords['kalibrierung'] > 0:
        score += 8
    if keywords['strömung'] > 0 or keywords['stromung'] > 0:
        score += 8
    
    # Supporting keywords
    if keywords['drift'] > 0:
        score += 5
    if keywords['resonanz'] > 0:
        score += 4
    if keywords['feld'] > 0:
        score += 3
    
    return min(score, 100.0)


# === ENDPOINT 1: PREDICT SCORE ===

@router.post("/predict-score")
def predict_score(request: PredictRequest):
    """
    🔮 PREDICT SCORE before processing!
    
    Analyzes prompt and predicts quality score based on:
    - Keyword presence (tier, drift, kalibrierung...)
    - Text length
    - Topic-style combination
    - Historical data
    """
    
    prompt = request.prompt_text
    topic = request.topic
    style = request.style
    wrapper = request.wrapper
    
    # Extract features
    keywords = extract_keywords(prompt)
    length = len(prompt)
    
    # Calculate keyword score
    keyword_score = calculate_keyword_score(keywords)
    
    # Length score (optimal: 1500-3000 chars)
    if length < 500:
        length_score = 50
    elif length < 1500:
        length_score = 70
    elif length < 3000:
        length_score = 90
    else:
        length_score = 80
    
    # Load historical data for topic+style
    processed = load_all_processed()
    
    topic_style_scores = []
    for p in processed:
        p_topic = p.get('filename', '').split('__topic_')[1].split('__')[0] if '__topic_' in p.get('filename', '') else ''
        p_style = p.get('filename', '').split('__style_')[1].split('.')[0] if '__style_' in p.get('filename', '') else ''
        
        if p_topic == topic and p_style == style:
            result = p.get('syntex_result', {})
            if result:
                score = result.get('quality_score', {})
                if isinstance(score, dict):
                    total = score.get('total_score', 0)
                    if total:
                        topic_style_scores.append(total)
    
    # Historical average for this topic+style
    historical_avg = sum(topic_style_scores) / len(topic_style_scores) if topic_style_scores else 70
    
    # Weighted prediction
    predicted_score = (
        keyword_score * 0.5 +      # Keywords most important!
        length_score * 0.2 +        # Length matters
        historical_avg * 0.3        # Historical context
    )
    
    # Confidence calculation
    confidence = "LOW"
    if len(topic_style_scores) > 10:
        if keywords['tier'] > 0 or keywords['driftkörper'] > 0:
            confidence = "HIGH"
        else:
            confidence = "MEDIUM"
    
    # Suggestions
    suggestions = []
    if keywords['tier'] == 0:
        suggestions.append("Add 'TIER-1/2/3/4' structure for +15 points!")
    if keywords['driftkörper'] == 0:
        suggestions.append("Add 'Driftkörper' keyword for +10 points!")
    if keywords['kalibrierung'] == 0:
        suggestions.append("Add 'Kalibrierung' keyword for +8 points!")
    if length < 1500:
        suggestions.append("Increase length to 1500-3000 chars for better score")
    
    return {
        "status": "SCORE_PREDICTED",
        "predicted_score": round(predicted_score, 2),
        "confidence": confidence,
        "breakdown": {
            "keyword_contribution": round(keyword_score * 0.5, 2),
            "length_contribution": round(length_score * 0.2, 2),
            "historical_contribution": round(historical_avg * 0.3, 2)
        },
        "analysis": {
            "prompt_length": length,
            "keywords_found": {k: v for k, v in keywords.items() if v > 0},
            "total_keywords": sum(keywords.values()),
            "historical_avg_for_topic_style": round(historical_avg, 2),
            "sample_size": len(topic_style_scores)
        },
        "suggestions": suggestions,
        "recommendation": "PROCESS" if predicted_score > 70 else "IMPROVE_FIRST"
    }




# === ENDPOINT 2: FIELD MISSING ANALYSIS ===

@router.get("/fields-missing-analysis")
def fields_missing_analysis():
    """
    🔍 ANALYZE WHY FIELDS ARE MISSING
    
    Shows which fields are NOT being detected and examples why.
    Critical for fixing DRUCKFAKTOREN 0.81% problem!
    """
    
    processed = load_all_processed()
    
    # Track field detection
    field_stats = {
        'DRIFTKORPER': {'detected': 0, 'missing': 0, 'examples': []},
        'KALIBRIERUNG': {'detected': 0, 'missing': 0, 'examples': []},
        'STROMUNG': {'detected': 0, 'missing': 0, 'examples': []},
        'HINTERGRUND_MUSTER': {'detected': 0, 'missing': 0, 'examples': []},
        'DRUCKFAKTOREN': {'detected': 0, 'missing': 0, 'examples': []},
        'TIEFE': {'detected': 0, 'missing': 0, 'examples': []}
    }
    
    for p in processed:
        result = p.get('syntex_result', {})
        if not result:
            continue
            
        score = result.get('quality_score', {})
        if not isinstance(score, dict):
            continue
            
        breakdown = score.get('detail_breakdown', {})
        filename = p.get('filename', '')
        
        # Check each field
        for field_key, field_name in [
            ('driftkorper', 'DRIFTKORPER'),
            ('kalibrierung', 'KALIBRIERUNG'),
            ('stromung', 'STROMUNG'),
            ('hintergrund_muster', 'HINTERGRUND_MUSTER'),
            ('druckfaktoren', 'DRUCKFAKTOREN'),
            ('tiefe', 'TIEFE')
        ]:
            if breakdown.get(field_key):
                field_stats[field_name]['detected'] += 1
            else:
                field_stats[field_name]['missing'] += 1
                # Save example (first 5)
                if len(field_stats[field_name]['examples']) < 5:
                    field_stats[field_name]['examples'].append({
                        'filename': filename,
                        'score': score.get('total_score', 0),
                        'other_fields_detected': [k for k, v in breakdown.items() if v]
                    })
    
    # Calculate rates
    for field in field_stats:
        total = field_stats[field]['detected'] + field_stats[field]['missing']
        if total > 0:
            field_stats[field]['detection_rate'] = round(
                (field_stats[field]['detected'] / total) * 100, 2
            )
        else:
            field_stats[field]['detection_rate'] = 0
    
    # Sort by detection rate (lowest first = biggest problems!)
    sorted_fields = sorted(
        field_stats.items(),
        key=lambda x: x[1]['detection_rate']
    )
    
    return {
        "status": "FIELD_MISSING_ANALYSIS",
        "total_jobs_analyzed": len(processed),
        "fields_by_detection_rate": [
            {
                "field": field,
                "detection_rate": stats['detection_rate'],
                "detected_count": stats['detected'],
                "missing_count": stats['missing'],
                "severity": (
                    "CRITICAL" if stats['detection_rate'] < 10 else
                    "HIGH" if stats['detection_rate'] < 50 else
                    "MEDIUM" if stats['detection_rate'] < 80 else
                    "LOW"
                ),
                "example_failures": stats['examples']
            }
            for field, stats in sorted_fields
        ],
        "insights": [
            f"🔥 {field}: Only {stats['detection_rate']:.1f}% detected!"
            for field, stats in sorted_fields[:3]
        ]
    }




# === ENDPOINT 3: KEYWORD COMBINATIONS ===

@router.get("/keyword-combinations")
def keyword_combinations():
    """
    🔥 FIND THE POWER COMBOS!
    
    Which keyword combinations create the HIGHEST scores?
    "drift + kalibrierung" = 98.5?
    "tier-1 + driftkörper" = 99.2?
    
    This is GOLD for evolution! 💎
    """
    
    processed = load_all_processed()
    
    # Track combinations
    combos = {}
    
    for p in processed:
        # Get prompt text
        filename = p.get('filename', '')
        prompt_file = PROCESSED_DIR / filename
        
        if not prompt_file.exists():
            continue
            
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt_text = f.read().lower()
        except:
            continue
        
        # Get score
        result = p.get('syntex_result', {})
        if not result:
            continue
        score_data = result.get('quality_score', {})
        if not isinstance(score_data, dict):
            continue
        total_score = score_data.get('total_score', 0)
        if not total_score:
            continue
        
        # Extract keywords present
        keywords_present = []
        if 'tier-' in prompt_text:
            keywords_present.append('tier')
        if 'driftkörper' in prompt_text or 'driftkorper' in prompt_text:
            keywords_present.append('driftkörper')
        if 'drift' in prompt_text and 'driftkörper' not in keywords_present:
            keywords_present.append('drift')
        if 'kalibrierung' in prompt_text:
            keywords_present.append('kalibrierung')
        if 'strömung' in prompt_text or 'stromung' in prompt_text:
            keywords_present.append('strömung')
        if 'resonanz' in prompt_text:
            keywords_present.append('resonanz')
        if 'feld' in prompt_text:
            keywords_present.append('feld')
        
        # Generate all 2-keyword combinations
        for i in range(len(keywords_present)):
            for j in range(i+1, len(keywords_present)):
                combo = tuple(sorted([keywords_present[i], keywords_present[j]]))
                combo_str = ' + '.join(combo)
                
                if combo_str not in combos:
                    combos[combo_str] = []
                combos[combo_str].append(total_score)
    
    # Calculate averages
    combo_stats = []
    for combo, scores in combos.items():
        if len(scores) >= 3:  # At least 3 samples
            avg_score = sum(scores) / len(scores)
            combo_stats.append({
                'combination': combo,
                'avg_score': round(avg_score, 2),
                'sample_count': len(scores),
                'min_score': min(scores),
                'max_score': max(scores),
                'power_rating': (
                    '🔥🔥🔥' if avg_score > 95 else
                    '🔥🔥' if avg_score > 85 else
                    '🔥' if avg_score > 75 else
                    '💧'
                )
            })
    
    # Sort by avg score
    combo_stats.sort(key=lambda x: x['avg_score'], reverse=True)
    
    return {
        "status": "KEYWORD_COMBINATIONS",
        "total_combinations_found": len(combo_stats),
        "top_combinations": combo_stats[:20],
        "insights": [
            f"💎 Best combo: {combo_stats[0]['combination']} = {combo_stats[0]['avg_score']} avg!",
            f"🔥 Top 3 combos all score {sum(c['avg_score'] for c in combo_stats[:3])/3:.1f}+ average!",
            f"⚡ {len([c for c in combo_stats if c['avg_score'] > 90])} combos break 90+ barrier!"
        ] if combo_stats else ["No sufficient data yet"]
    }




# === ENDPOINT 4: PROMPT TEMPLATES ===

@router.get("/templates-by-score")
def templates_by_score(min_score: float = 90):
    """
    📚 TEMPLATES FROM THE BEST!
    
    Extract patterns from high-scoring prompts.
    Learn the STRUCTURE, KEYWORDS, LENGTH that works!
    
    This is how the system LEARNS! 🧠
    """
    
    processed = load_all_processed()
    
    high_scorers = []
    
    for p in processed:
        # Get score
        result = p.get('syntex_result', {})
        if not result:
            continue
        score_data = result.get('quality_score', {})
        if not isinstance(score_data, dict):
            continue
        total_score = score_data.get('total_score', 0)
        
        if total_score < min_score:
            continue
        
        # Get prompt text
        filename = p.get('filename', '')
        prompt_file = PROCESSED_DIR / filename
        
        if not prompt_file.exists():
            continue
            
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt_text = f.read()
        except:
            continue
        
        # Extract metadata
        topic = filename.split('__topic_')[1].split('__')[0] if '__topic_' in filename else 'unknown'
        style = filename.split('__style_')[1].split('.')[0] if '__style_' in filename else 'unknown'
        
        # Extract keywords
        keywords = extract_keywords(prompt_text)
        
        high_scorers.append({
            'filename': filename,
            'score': total_score,
            'topic': topic,
            'style': style,
            'length': len(prompt_text),
            'prompt_preview': prompt_text[:300] + '...' if len(prompt_text) > 300 else prompt_text,
            'keywords': {k: v for k, v in keywords.items() if v > 0},
            'total_keywords': sum(keywords.values()),
            'field_breakdown': score_data.get('detail_breakdown', {})
        })
    
    # Sort by score
    high_scorers.sort(key=lambda x: x['score'], reverse=True)
    
    # Extract patterns
    if high_scorers:
        avg_length = sum(h['length'] for h in high_scorers) / len(high_scorers)
        avg_keywords = sum(h['total_keywords'] for h in high_scorers) / len(high_scorers)
        
        # Most common keywords
        all_keywords = {}
        for h in high_scorers:
            for k, v in h['keywords'].items():
                all_keywords[k] = all_keywords.get(k, 0) + v
        
        common_keywords = sorted(all_keywords.items(), key=lambda x: x[1], reverse=True)[:10]
        
        patterns = {
            'avg_length': round(avg_length, 0),
            'avg_keywords_count': round(avg_keywords, 1),
            'length_range': f"{min(h['length'] for h in high_scorers)}-{max(h['length'] for h in high_scorers)} chars",
            'most_common_keywords': [{'keyword': k, 'total_occurrences': v} for k, v in common_keywords]
        }
    else:
        patterns = {}
    
    return {
        "status": "PROMPT_TEMPLATES",
        "min_score_filter": min_score,
        "templates_found": len(high_scorers),
        "top_templates": high_scorers[:10],
        "patterns": patterns,
        "insights": [
            f"💎 {len(high_scorers)} prompts score {min_score}+!",
            f"📏 Optimal length: ~{patterns.get('avg_length', 0)} chars",
            f"🔑 Average {patterns.get('avg_keywords_count', 0)} keywords per prompt",
            f"🔥 Top keyword: {patterns.get('most_common_keywords', [{}])[0].get('keyword', 'N/A') if patterns.get('most_common_keywords') else 'N/A'}"
        ] if patterns else ["No templates found at this score level"]
    }




# === ENDPOINT 5: OPTIMAL WRAPPER PER TOPIC ===

@router.get("/optimal-wrapper-for-topic")
def optimal_wrapper_for_topic():
    """
    🎯 WHICH WRAPPER FOR WHICH TOPIC?
    
    kritisch → SYNTEX? (best performance)
    harmlos → DEEPSWEEP? (cheaper, good enough)
    
    OPTIMIZE your processing! 💰⚡
    """
    
    processed = load_all_processed()
    
    # Track wrapper performance per topic
    topic_wrapper_stats = {}
    
    for p in processed:
        # Extract topic
        filename = p.get('filename', '')
        if '__topic_' not in filename:
            continue
        topic = filename.split('__topic_')[1].split('__')[0]
        
        # Get wrapper and score
        result = p.get('syntex_result', {})
        if not result:
            continue
        wrapper = result.get('wrapper', 'unknown')
        
        score_data = result.get('quality_score', {})
        if not isinstance(score_data, dict):
            continue
        total_score = score_data.get('total_score', 0)
        if not total_score:
            continue
        
        # Track
        if topic not in topic_wrapper_stats:
            topic_wrapper_stats[topic] = {}
        if wrapper not in topic_wrapper_stats[topic]:
            topic_wrapper_stats[topic][wrapper] = []
        
        topic_wrapper_stats[topic][wrapper].append(total_score)
    
    # Calculate averages and recommendations
    recommendations = []
    
    for topic, wrappers in topic_wrapper_stats.items():
        wrapper_avgs = {}
        for wrapper, scores in wrappers.items():
            if len(scores) >= 3:  # Min 3 samples
                wrapper_avgs[wrapper] = {
                    'avg_score': round(sum(scores) / len(scores), 2),
                    'sample_count': len(scores),
                    'min_score': min(scores),
                    'max_score': max(scores)
                }
        
        if not wrapper_avgs:
            continue
        
        # Find best wrapper
        best_wrapper = max(wrapper_avgs.items(), key=lambda x: x[1]['avg_score'])
        
        # All wrappers for this topic
        all_wrappers = sorted(
            wrapper_avgs.items(),
            key=lambda x: x[1]['avg_score'],
            reverse=True
        )
        
        recommendations.append({
            'topic': topic,
            'best_wrapper': best_wrapper[0],
            'best_avg_score': best_wrapper[1]['avg_score'],
            'all_wrappers': [
                {
                    'wrapper': w,
                    'avg_score': stats['avg_score'],
                    'sample_count': stats['sample_count'],
                    'performance_rating': (
                        '🔥🔥🔥' if stats['avg_score'] > 90 else
                        '🔥🔥' if stats['avg_score'] > 80 else
                        '🔥' if stats['avg_score'] > 70 else
                        '💧'
                    )
                }
                for w, stats in all_wrappers
            ]
        })
    
    # Sort by best score
    recommendations.sort(key=lambda x: x['best_avg_score'], reverse=True)
    
    return {
        "status": "OPTIMAL_WRAPPER_ANALYSIS",
        "topics_analyzed": len(recommendations),
        "recommendations": recommendations,
        "insights": [
            f"💎 Best overall: {recommendations[0]['topic']} with {recommendations[0]['best_wrapper']} = {recommendations[0]['best_avg_score']}",
            f"🔥 {len([r for r in recommendations if r['best_avg_score'] > 80])} topics break 80+ with optimal wrapper",
            f"⚡ Use {recommendations[0]['best_wrapper']} for best results!"
        ] if recommendations else ["Not enough data yet"]
    }




# === ENDPOINT 6: EVOLUTION LEARNING CURVE ===

@router.get("/evolution-learning-curve")
def evolution_learning_curve():
    """
    🧠 SEE THE SYSTEM LEARN!
    
    Track how prompts improve over time.
    Early prompts vs Late prompts.
    The EVOLUTION in action! 📈
    
    This is PROOF that SYNTX learns! 💎
    """
    
    processed = load_all_processed()
    
    # Group by date
    from datetime import datetime
    
    daily_stats = {}
    
    for p in processed:
        filename = p.get('filename', '')
        if not filename:
            continue
        
        # Extract date from filename (format: YYYYMMDD_HHMMSS_...)
        try:
            date_str = filename[:8]  # YYYYMMDD
            date = datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m-%d')
        except:
            continue
        
        # Get score
        result = p.get('syntex_result', {})
        if not result:
            continue
        score_data = result.get('quality_score', {})
        if not isinstance(score_data, dict):
            continue
        total_score = score_data.get('total_score', 0)
        if not total_score:
            continue
        
        # Track
        if date not in daily_stats:
            daily_stats[date] = {'scores': [], 'count': 0, 'perfect_count': 0}
        
        daily_stats[date]['scores'].append(total_score)
        daily_stats[date]['count'] += 1
        if total_score >= 95:
            daily_stats[date]['perfect_count'] += 1
    
    # Calculate daily averages
    timeline = []
    for date in sorted(daily_stats.keys()):
        stats = daily_stats[date]
        avg_score = sum(stats['scores']) / len(stats['scores'])
        
        timeline.append({
            'date': date,
            'avg_score': round(avg_score, 2),
            'prompt_count': stats['count'],
            'perfect_count': stats['perfect_count'],
            'perfect_rate': round((stats['perfect_count'] / stats['count']) * 100, 1),
            'min_score': min(stats['scores']),
            'max_score': max(stats['scores']),
            'trend': '📈' if len(timeline) > 0 and avg_score > timeline[-1]['avg_score'] else '📉'
        })
    
    # Calculate overall trend
    if len(timeline) >= 2:
        first_week_avg = sum(t['avg_score'] for t in timeline[:7]) / min(7, len(timeline))
        last_week_avg = sum(t['avg_score'] for t in timeline[-7:]) / min(7, len(timeline[-7:]))
        improvement = last_week_avg - first_week_avg
        
        learning_velocity = improvement / len(timeline) if len(timeline) > 0 else 0
    else:
        first_week_avg = 0
        last_week_avg = 0
        improvement = 0
        learning_velocity = 0
    
    return {
        "status": "EVOLUTION_LEARNING_CURVE",
        "days_tracked": len(timeline),
        "timeline": timeline,
        "overall_trend": {
            "first_week_avg": round(first_week_avg, 2),
            "last_week_avg": round(last_week_avg, 2),
            "total_improvement": round(improvement, 2),
            "learning_velocity": round(learning_velocity, 3),
            "direction": "📈 IMPROVING" if improvement > 0 else "📉 DECLINING" if improvement < 0 else "➡️ STABLE"
        },
        "insights": [
            f"🧠 System learning velocity: {abs(learning_velocity):.3f} points/day",
            f"📈 Total improvement: {improvement:+.2f} points" if improvement != 0 else "➡️ Performance stable",
            f"💎 Best day: {max(timeline, key=lambda x: x['avg_score'])['date']} with {max(timeline, key=lambda x: x['avg_score'])['avg_score']} avg",
            f"🔥 Current trend: {timeline[-1]['trend'] if timeline else '?'}"
        ] if timeline else ["Not enough data yet"]
    }


