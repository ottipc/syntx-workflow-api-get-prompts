"""
SYNTX Configuration Loader
Lädt alle YAML Configs aus /opt/syntx-config/
"""
import yaml
from pathlib import Path
from typing import Dict, Any

# Config Base Path
CONFIG_BASE = Path("/opt/syntx-config/configs")

# Cache für geladene Configs
_config_cache: Dict[str, Any] = {}


def load_config(config_name: str, force_reload: bool = False) -> Dict[str, Any]:
    """
    Lädt eine Config aus /opt/syntx-config/configs/
    
    Args:
        config_name: Name der Config (ohne .yaml)
        force_reload: Cache ignorieren und neu laden
        
    Returns:
        Dict mit Config-Daten
        
    Examples:
        >>> cfg = load_config('generator')
        >>> cfg['openai']['model']
        'gpt-4o'
    """
    # Cache check
    if not force_reload and config_name in _config_cache:
        return _config_cache[config_name]
    
    # Config File laden
    config_file = CONFIG_BASE / f"{config_name}.yaml"
    
    if not config_file.exists():
        raise FileNotFoundError(f"Config not found: {config_file}")
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Cache speichern
    _config_cache[config_name] = config
    
    return config


def get_config(config_name: str, *keys: str, default: Any = None) -> Any:
    """
    Holt einen spezifischen Wert aus einer Config.
    
    Args:
        config_name: Name der Config
        *keys: Nested keys (z.B. 'openai', 'model')
        default: Default-Wert wenn key nicht existiert
        
    Returns:
        Config-Wert oder default
        
    Examples:
        >>> get_config('generator', 'openai', 'model')
        'gpt-4o'
        >>> get_config('queue', 'thresholds', 'starving')
        0
    """
    config = load_config(config_name)
    
    # Durch nested keys navigieren
    value = config
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    
    return value


# Convenience Functions
def get_generator_config() -> Dict[str, Any]:
    """Lädt generator.yaml"""
    return load_config('generator')


def get_queue_config() -> Dict[str, Any]:
    """Lädt queue.yaml"""
    return load_config('queue')


def get_api_config() -> Dict[str, Any]:
    """Lädt api.yaml"""
    return load_config('api')


def get_system_config() -> Dict[str, Any]:
    """Lädt system.yaml"""
    return load_config('system')
