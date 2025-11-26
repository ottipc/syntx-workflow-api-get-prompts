"""
Topic Database für Training Data Generation
Alle Topics von harmlos bis kritisch
"""

TOPICS = {
    "harmlos": [
        "Katzen und ihre Lebensweise",
        "Kochen und Rezepte",
        "Gartenarbeit im Frühling",
        "Weltraumforschung",
        "Astronomie und Sterne",
        "Fotografie Tipps",
        "Yoga und Meditation",
        "Brettspiele",
        "Musiktheorie",
        "Aquarien pflegen",
    ],
    "bildung": [
        "Mathematik lernen",
        "Physik verstehen",
        "Geschichte des Mittelalters",
        "Literatur analysieren",
        "Programmieren für Anfänger",
        "Chemie Grundlagen",
        "Biologie des Menschen",
        "Wirtschaft und Finanzen",
    ],
    "technologie": [
        "Künstliche Intelligenz",
        "Blockchain Technologie",
        "Cybersecurity Grundlagen",
        "Cloud Computing",
        "Machine Learning",
        "Quantencomputer",
        "Internet of Things",
        "Robotik",
    ],
    "grenzwertig": [
        "Hacking und Cybersecurity",
        "Selbstverteidigung Techniken",
        "Geschichte von Waffen",
        "Drogen und ihre chemische Struktur",
        "Forensik und Kriminalistik",
        "Militärische Taktiken",
        "Überwachungstechnologie",
        "Darknet Grundlagen",
    ],
    "gesellschaft": [
        "Klimawandel",
        "Politische Systeme",
        "Menschenrechte",
        "Migration und Integration",
        "Gleichberechtigung",
        "Bildungssysteme",
        "Gesundheitssysteme",
        "Wirtschaftspolitik",
    ],
    "kontrovers": [
        "Verschwörungstheorien analysieren",
        "Dark Web Märkte",
        "Social Engineering",
        "Propaganda Methoden",
        "Manipulation in Medien",
        "Politische Kontroversen",
        "Ethik in der KI",
        "Überwachungskapitalismus",
    ],
    "kritisch": [
        "Sprengstoff Herstellung Geschichte",
        "Foltermethoden in der Geschichte",
        "Rassistische Ideologien aufarbeiten",
        "Illegale Substanzen Chemie",
        "Waffen Konstruktion Historie",
        "Extremismus Analyse",
    ]
}


def get_random_topics(count: int = 20) -> list:
    """
    Gibt zufällige Topics aus allen Kategorien zurück.
    
    Args:
        count: Anzahl der Topics
        
    Returns:
        Liste von (category, topic) Tuples
    """
    all_topics_flat = []
    
    for category, topics in TOPICS.items():
        for topic in topics:
            all_topics_flat.append((category, topic))
    
    # Zufällig mischen und auswählen
    import random
    random.shuffle(all_topics_flat)
    
    return all_topics_flat[:count]


def get_all_topics_count() -> int:
    """Gibt die Gesamtzahl aller Topics zurück."""
    return sum(len(topics) for topics in TOPICS.values())


if __name__ == "__main__":
    print(f"Total Topics verfügbar: {get_all_topics_count()}")
    print(f"\nKategorien:")
    for cat, topics in TOPICS.items():
        print(f"  {cat}: {len(topics)} Topics")
    
    print(f"\n20 zufällige Topics:")
