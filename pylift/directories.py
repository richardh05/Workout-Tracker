from pathlib import Path
import sys

def _getDefaultDb() -> Path:
    """
    Finds the user's 'Documents' folder across different operating systems
    """
    if sys.platform == "win32":
        # Windows: Documents folder is usually directly under the user profile
        import ctypes
        from ctypes import wintypes
        CSIDL_PERSONAL = 5       # My Documents
        SHGFP_TYPE_CURRENT = 0   # Get current, not default value
        buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
        return Path(buf.value) / "gym.sqlite"
    elif sys.platform == "darwin":
        # macOS: Documents is under the user's home directory
        return Path.home() / "Documents"
    else:
        # Linux/Unix: Documents is usually under the user's home directory
        # This is a common XDG Base Directory specification, but not universally guaranteed.
        # For simplicity, we'll assume it's directly under home for now.
        return Path.home() / "Documents"
    
def getDefaultDb() -> Path:
    """
    Returns the default path to the SQLite database file.
    
    This function checks the operating system and returns a path to a default
    SQLite database file named 'gym.sqlite' in the user's 'Documents' folder.
    
    :return: Path to the default SQLite database file.
    """
    return _getDefaultDb() / "gym.sqlite"