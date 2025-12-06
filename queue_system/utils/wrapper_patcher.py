"""
SYNTX Wrapper Patcher
Patcht den Calibrator zur Laufzeit um alle Wrappers zu nutzen
"""
from pathlib import Path
import sys

# Config laden
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config.config_loader import get_config


def patch_wrapper_system():
    """
    Patcht syntex_injector.syntex.core.wrapper zur Laufzeit
    um alle Wrappers aus /opt/syntx-config/wrappers/ zu nutzen
    """
    import syntex_injector.syntex.core.wrapper as wrapper_module
    
    # Wrapper Dir aus Config
    wrapper_dir = Path(get_config('system', 'paths', 'wrappers'))
    
    # Alle Wrappers finden
    available = {}
    for wrapper_file in wrapper_dir.glob("syntex_wrapper_*.txt"):
        name = wrapper_file.stem.replace("syntex_wrapper_", "")
        available[name] = wrapper_file
    
    # Patch!
    wrapper_module.WRAPPER_DIR = wrapper_dir
    wrapper_module.AVAILABLE_WRAPPERS = available
    
    return available


def get_available_wrappers():
    """Liste aller verfügbaren Wrappers"""
    wrapper_dir = Path(get_config('system', 'paths', 'wrappers'))
    
    wrappers = []
    for wrapper_file in wrapper_dir.glob("syntex_wrapper_*.txt"):
        name = wrapper_file.stem.replace("syntex_wrapper_", "")
        wrappers.append(name)
    
    return sorted(wrappers)


if __name__ == "__main__":
    print("🔧 Wrapper Patcher Test\n")
    
    available = patch_wrapper_system()
    
    print(f"✅ Patched! Found {len(available)} wrappers:")
    for name in sorted(available.keys()):
        print(f"   - {name}")
