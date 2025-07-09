from pathlib import Path
import sys
import os

def get_config_dir(app_name: str = "PyLift") -> Path:
    """
    Returns the standard user configuration directory for the application
    across Linux, macOS, and Windows.
    """
    if sys.platform.startswith('win'):
        config_root = os.getenv('APPDATA', Path.home() / 'AppData' / 'Roaming')
        p = Path(config_root) / app_name
    elif sys.platform == 'darwin':
        p = Path.home() / 'Library' / 'Application Support' / app_name
    else:
        # Linux & other Unix-like systems
        p = Path.home() / '.config' / app_name.lower()
    p.mkdir(parents=True, exist_ok=True)
    return p


def get_data_dir() -> Path:
    """
    Return the default data storage directory for the app,
    following OS conventions.
    """
    if sys.platform.startswith('win'):
        p = Path(os.getenv('LOCALAPPDATA', Path.home() / 'AppData' / 'Local' / 'PyLift'))
    elif sys.platform == 'darwin':
        p = Path.home() / 'Library' / 'Application Support' / 'PyLift'
    else:  # assume Linux and other UNIX-like
        p = Path.home() / '.local' / 'share' / 'pylift'
    
    p.mkdir(parents=True, exist_ok=True)
    return p

def get_cache_dir() -> Path:
    """
    Return the default cache directory for the app,
    following OS conventions.
    """
    if sys.platform.startswith('win'):
        p = Path(os.getenv('LOCALAPPDATA', Path.home() / 'AppData' / 'Local')) / 'PyLift' / 'Cache'
    elif sys.platform == 'darwin':
        p = Path.home() / 'Library' / 'Caches / PyLift'
    else:  # assume Linux and other UNIX-like
        p = Path.home() / '.cache' / 'pylift'
    
    p.mkdir(parents=True, exist_ok=True)
    return p

def get_tests_dir() -> Path: return get_cache_dir() / 'tests'