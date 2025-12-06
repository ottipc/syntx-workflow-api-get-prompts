"""
Prompt Quality Scoring System
Bewertet generierte Prompts nach mehreren Kriterien
"""


def score_prompt(text: str) -> dict:
    """
    Bewertet die Qualität eines generierten Prompts.
    
    Score-Kriterien:
    - Länge (optimal: 100-500 Zeichen)
    - Komplexität (Anzahl Sätze, Wörter)
    - Struktur (hat Absätze, Aufzählungen)
    - Klarheit (durchschnittliche Wortlänge)
    
    Returns:
        dict mit einzelnen Scores und Gesamt-Score (0-10)
    """
    if not text:
        return {
            "length_score": 0,
            "complexity_score": 0,
            "structure_score": 0,
            "clarity_score": 0,
            "total_score": 0.0,
            "max_score": 10,
            "quality_rating": "sehr schlecht"
        }
    
    # 1. Längen-Score (0-3 Punkte)
    length = len(text)
    if 100 <= length <= 500:
        length_score = 3
    elif 50 <= length < 100 or 500 < length <= 800:
        length_score = 2
    elif length < 50 or length > 1000:
        length_score = 0
    else:
        length_score = 1
    
    # 2. Komplexitäts-Score (0-3 Punkte)
    sentences = text.count('.') + text.count('!') + text.count('?')
    words = len(text.split())
    
    if sentences >= 3 and words >= 50:
        complexity_score = 3
    elif sentences >= 2 and words >= 30:
        complexity_score = 2
    elif sentences >= 1:
        complexity_score = 1
    else:
        complexity_score = 0
    
    # 3. Struktur-Score (0-2 Punkte)
    has_newlines = '\n' in text
    has_lists = any(marker in text for marker in ['- ', '* ', '1.', '2.'])
    
    structure_score = 0
    if has_newlines:
        structure_score += 1
    if has_lists:
        structure_score += 1
    
    # 4. Klarheits-Score (0-2 Punkte)
    avg_word_length = sum(len(word) for word in text.split()) / max(len(text.split()), 1)
    
    if 4 <= avg_word_length <= 7:
        clarity_score = 2
    elif 3 <= avg_word_length < 4 or 7 < avg_word_length <= 9:
        clarity_score = 1
    else:
        clarity_score = 0
    
    # Gesamt-Score (0-10)
    total_score = length_score + complexity_score + structure_score + clarity_score
    
    # Quality Rating
    if total_score >= 9:
        quality_rating = "excellent"
    elif total_score >= 7:
        quality_rating = "gut"
    elif total_score >= 5:
        quality_rating = "okay"
    elif total_score >= 3:
        quality_rating = "schwach"
    else:
        quality_rating = "sehr schlecht"
    
    return {
        "length_score": length_score,
        "complexity_score": complexity_score,
        "structure_score": structure_score,
        "clarity_score": clarity_score,
        "total_score": total_score,
        "max_score": 10,
        "quality_rating": quality_rating,
        "stats": {
            "length": length,
            "sentences": sentences,
            "words": words,
            "avg_word_length": round(avg_word_length, 2)
        }
    }


if __name__ == "__main__":
    # Test
    test_text = """Dies ist ein Beispiel-Prompt über künstliche Intelligenz.
    Er enthält mehrere Sätze und ist gut strukturiert.
    - Punkt 1: Technologie
    - Punkt 2: Innovation
    Das macht ihn zu einem qualitativ hochwertigen Prompt."""
    
    score = score_prompt(test_text)
    print(f"Score: {score['total_score']}/{score['max_score']} - {score['quality_rating']}")
    print(f"Details: {score}")
