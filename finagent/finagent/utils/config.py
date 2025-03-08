import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

# Define the location for configuration
def get_config_dir() -> Path:
    """Get the directory for configuration files."""
    # First check for XDG_CONFIG_HOME
    if "XDG_CONFIG_HOME" in os.environ:
        config_dir = Path(os.environ["XDG_CONFIG_HOME"]) / "finagent"
    # Otherwise use platform-specific default
    else:
        home = Path.home()
        if os.name == "nt":  # Windows
            config_dir = Path(os.environ.get("APPDATA", str(home / "AppData" / "Roaming"))) / "finagent"
        else:  # Unix-like
            config_dir = home / ".config" / "finagent"
            
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir

def get_config_path() -> Path:
    """Get the path to the configuration file."""
    return get_config_dir() / "config.json"

def get_config() -> Dict[str, Any]:
    """Get the configuration dictionary."""
    config_path = get_config_path()
    if config_path.exists():
        with open(config_path, "r") as f:
            return json.load(f)
    else:
        # Return default configuration
        return {
            "news_provider": "newsapi,gnewsapi",
            "storage_type": "json"
        }

def set_config(key: str, value: Any) -> None:
    """Set a configuration value."""
    config = get_config()
    config[key] = value
    
    config_path = get_config_path()
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)