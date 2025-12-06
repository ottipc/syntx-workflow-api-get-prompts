"""
Topics Database - Config-Driven
Lädt Topics aus /opt/syntx-config/configs/generator.yaml
"""
import random
from typing import List, Tuple
import sys
from pathlib import Path

# Add parent to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config_loader import get_config


def get_all_topics() -> List[Tuple[str, str]]:
    """
    Holt alle Topics aus Config.
    
    Returns:
        List of (category, topic) tuples
    """
    topics_config = get_config('generator', 'topics')
    
    all_topics = []
    for category, topic_list in topics_config.items():
        for topic in topic_list:
            all_topics.append((category, topic))
    
    return all_topics


def get_random_topics(count: int = 20) -> List[Tuple[str, str]]:
    """
    Holt zufällige Topics aus Config.
    
    Args:
        count: Anzahl Topics
        
    Returns:
        List of (category, topic) tuples
    """
    all_topics = get_all_topics()
    
    # Wenn mehr requested als verfügbar, nimm alle
    if count >= len(all_topics):
        selected = all_topics.copy()
        random.shuffle(selected)
        return selected
    
    # Zufällige Auswahl
    return random.sample(all_topics, count)


def get_topics_by_category(category: str) -> List[str]:
    """
    Holt alle Topics einer Kategorie.
    
    Args:
        category: Kategorie-Name
        
    Returns:
        List of topic names
    """
    return get_config('generator', 'topics', category, default=[])


def get_all_categories() -> List[str]:
    """
    Holt alle verfügbaren Kategorien.
    
    Returns:
        List of category names
    """
    topics_config = get_config('generator', 'topics')
    return list(topics_config.keys())


if __name__ == "__main__":
    # Test
    print("📚 Topics Database (Config-Driven)\n")
    
    categories = get_all_categories()
    print(f"Categories: {categories}\n")
    
    all_topics = get_all_topics()
    print(f"Total Topics: {len(all_topics)}\n")
    
    random_topics = get_random_topics(5)
    print("Random 5 Topics:")
    for cat, topic in random_topics:
        print(f"  [{cat}] {topic}")
