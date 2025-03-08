import pluggy
from finagent import hookspecs

# Create a plugin manager
pm = pluggy.PluginManager("finagent")

# Add hook specifications to the plugin manager
pm.add_hookspecs(hookspecs)

def init_plugin_manager():
    """Initialize the plugin manager and load plugins."""
    # Register default hooks
    from . import default
    pm.register(default)
    
    # Register extension hooks
    from . import extensions
    pm.register(extensions)
    
    # Discover and register other plugins
    try:
        pm.load_setuptools_entrypoints("finagent")
    except Exception as e:
        # Log the error but continue
        print(f"Error loading plugins: {e}")
        
    return pm

def get_providers():
    """Get all registered providers."""
    providers = {
        "news_providers": [],
        "summarizers": []
    }
    
    # This is just a placeholder - in a real implementation,
    # we would collect all providers registered through hooks
    
    return providers