import os
from pathlib import Path
from typing import Union

def ensure_directory(directory: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory (Union[str, Path]): The directory path
        
    Returns:
        Path: The directory path as a Path object
    """
    if isinstance(directory, str):
        directory = Path(directory)
        
    directory.mkdir(parents=True, exist_ok=True)
    return directory

def get_data_dir() -> Path:
    """
    Get the data directory for storing application data.
    
    Returns:
        Path: The data directory
    """
    # First check for XDG_DATA_HOME
    if "XDG_DATA_HOME" in os.environ:
        data_dir = Path(os.environ["XDG_DATA_HOME"]) / "finagent"
    # Otherwise use platform-specific default
    else:
        home = Path.home()
        if os.name == "nt":  # Windows
            data_dir = Path(os.environ.get("LOCALAPPDATA", str(home / "AppData" / "Local"))) / "finagent"
        else:  # Unix-like
            data_dir = home / ".local" / "share" / "finagent"
            
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

def ensure_directory_exists(directory: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    This is an alias for ensure_directory.
    
    Args:
        directory (Union[str, Path]): The directory path
        
    Returns:
        Path: The directory path as a Path object
    """
    return ensure_directory(directory)

def ensure_dir_exists(directory: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    This is an alias for ensure_directory for backward compatibility.
    
    Args:
        directory (Union[str, Path]): The directory path
        
    Returns:
        Path: The directory path as a Path object
    """
    return ensure_directory(directory)