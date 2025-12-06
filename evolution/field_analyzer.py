"""
SYNTX Field Analyzer
Analysiert erfolgreiche Felder aus processed/ Queue
"""
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config_loader import get_config


class FieldAnalyzer:
    """Analysiert SYNTX Felder aus processed Jobs"""
    
    def __init__(self):
        self.config = get_config('evolution')
        self.queue_base = Path(get_config('queue', 'paths', 'base'))
        self.processed_dir = self.queue_base / "processed"
        self.archive_dir = self.queue_base / "archive"
        
    def get_top_processed_jobs(self, max_samples: int = 50, min_score: int = 90) -> List[Dict]:
        """
        Holt Top N processed Jobs mit Score >= min_score
        
        Returns:
            List of job dicts mit Metadata und Scores
        """
        jobs = []
        
        # Alle .json Files in processed/
        json_files = sorted(self.processed_dir.glob("*.json"))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    job_data = json.load(f)
                
                # Quality Score aus syntex_result
                syntex_result = job_data.get('syntex_result', {})
                quality = syntex_result.get('quality_score', {})
                total_score = quality.get('total_score', 0)
                
                if total_score >= min_score:
                    # TXT File mit Feldern laden
                    txt_file = json_file.with_suffix('.txt')
                    txt_content = ""
                    if txt_file.exists():
                        with open(txt_file, 'r') as tf:
                            txt_content = tf.read()
                    
                    jobs.append({
                        'file': json_file,
                        'score': total_score,
                        'topic': job_data.get('topic'),
                        'category': job_data.get('category'),
                        'style': job_data.get('style'),
                        'wrapper': syntex_result.get('wrapper'),
                        'field_completeness': quality.get('field_completeness', 0),
                        'structure_adherence': quality.get('structure_adherence', 0),
                        'fields_detected': quality.get('detail_breakdown', {}),
                        'txt_content': txt_content,
                        'gpt_quality': job_data.get('gpt_quality', {}),
                        'timestamp': job_data.get('processed_at')
                    })
                    
            except Exception as e:
                print(f"⚠️  Error reading {json_file}: {e}")
                continue
        
        # Sort by score (höchste zuerst)
        jobs.sort(key=lambda x: x['score'], reverse=True)
        
        # Top N
        return jobs[:max_samples]
    
    def analyze_patterns(self, jobs: List[Dict]) -> Dict[str, Any]:
        """
        Analysiert Patterns aus erfolgreichen Jobs
        
        Returns:
            {
                'avg_scores': {...},
                'patterns': [...],
                'recommendations': [...]
            }
        """
        if not jobs:
            return {
                'sample_count': 0,
                'patterns': [],
                'recommendations': []
            }
        
        # Score Statistics
        scores = [j['score'] for j in jobs]
        field_completeness = [j['field_completeness'] for j in jobs]
        structure_adherence = [j['structure_adherence'] for j in jobs]
        
        # Category & Style Distribution
        categories = {}
        styles = {}
        wrappers = {}
        
        for job in jobs:
            cat = job.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
            
            style = job.get('style', 'unknown')
            styles[style] = styles.get(style, 0) + 1
            
            wrapper = job.get('wrapper', 'unknown')
            wrappers[wrapper] = wrappers.get(wrapper, 0) + 1
        
        # Felder die immer detected wurden
        all_detected_fields = {}
        for job in jobs:
            for field, detected in job['fields_detected'].items():
                if detected:
                    all_detected_fields[field] = all_detected_fields.get(field, 0) + 1
        
        # Patterns extrahieren
        patterns = []
        
        # Top Categories
        top_categories = sorted(categories.items(), key=lambda x: -x[1])[:3]
        patterns.append(f"Top Categories: {', '.join([f'{c}({n})' for c, n in top_categories])}")
        
        # Top Styles
        top_styles = sorted(styles.items(), key=lambda x: -x[1])[:3]
        patterns.append(f"Top Styles: {', '.join([f'{s}({n})' for s, n in top_styles])}")
        
        # Wrapper Performance
        for wrapper, count in wrappers.items():
            patterns.append(f"Wrapper '{wrapper}': {count} successful jobs")
        
        # Field Detection
        for field, count in sorted(all_detected_fields.items(), key=lambda x: -x[1]):
            percentage = (count / len(jobs)) * 100
            patterns.append(f"Field '{field}': {percentage:.0f}% detection rate")
        
        # GPT Quality correlation
        gpt_scores = [j['gpt_quality'].get('total_score', 0) for j in jobs]
        if gpt_scores:
            avg_gpt = sum(gpt_scores) / len(gpt_scores)
            patterns.append(f"Avg GPT Quality: {avg_gpt:.1f}/10")
        
        # Recommendations
        recommendations = []
        recommendations.append(f"Focus on categories: {', '.join([c for c, n in top_categories])}")
        recommendations.append(f"Use styles: {', '.join([s for s, n in top_styles])}")
        
        if field_completeness:
            avg_fc = sum(field_completeness) / len(field_completeness)
            if avg_fc == 100:
                recommendations.append("Maintain 100% field completeness!")
        
        return {
            'sample_count': len(jobs),
            'avg_score': round(sum(scores) / len(scores), 2) if scores else 0,
            'score_range': [min(scores), max(scores)] if scores else [0, 0],
            'avg_field_completeness': round(sum(field_completeness) / len(field_completeness), 2) if field_completeness else 0,
            'avg_structure_adherence': round(sum(structure_adherence) / len(structure_adherence), 2) if structure_adherence else 0,
            'categories': categories,
            'styles': styles,
            'wrappers': wrappers,
            'patterns': patterns,
            'recommendations': recommendations,
            'analyzed_at': datetime.now().isoformat()
        }
    
    def archive_processed_jobs(self, jobs: List[Dict]) -> int:
        """
        Verschiebt analysierte Jobs nach archive/
        
        Returns:
            Anzahl archivierter Jobs
        """
        self.archive_dir.mkdir(exist_ok=True)
        
        archived = 0
        for job in jobs:
            try:
                file_path = job['file']
                txt_file = file_path.with_suffix('.txt')
                
                # Move JSON
                if file_path.exists():
                    archive_path = self.archive_dir / file_path.name
                    file_path.rename(archive_path)
                
                # Move TXT
                if txt_file.exists():
                    archive_txt = self.archive_dir / txt_file.name
                    txt_file.rename(archive_txt)
                
                archived += 1
                
            except Exception as e:
                print(f"⚠️  Archive error {file_path}: {e}")
                continue
        
        return archived


if __name__ == "__main__":
    # Test
    print("🧬 SYNTX Field Analyzer Test\n")
    
    analyzer = FieldAnalyzer()
    
    # Get top jobs
    jobs = analyzer.get_top_processed_jobs(max_samples=50, min_score=90)
    print(f"✅ Found {len(jobs)} high-quality jobs (score >= 90)\n")
    
    if jobs:
        # Analyze
        analysis = analyzer.analyze_patterns(jobs)
        
        print(f"📊 ANALYSIS:")
        print(f"   Sample Count: {analysis['sample_count']}")
        print(f"   Avg Score: {analysis['avg_score']}/100")
        print(f"   Score Range: {analysis['score_range']}")
        print(f"   Avg Field Completeness: {analysis['avg_field_completeness']}%")
        print(f"   Avg Structure Adherence: {analysis['avg_structure_adherence']}%")
        
        print(f"\n🔥 PATTERNS:")
        for pattern in analysis['patterns']:
            print(f"   - {pattern}")
        
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in analysis['recommendations']:
            print(f"   - {rec}")
    else:
        print("❌ No jobs found with score >= 90")
