import pluggy

# Define the namespace for our hooks
hookspec = pluggy.HookspecMarker("finagent")
hookimpl = pluggy.HookimplMarker("finagent")

# Define a hook specification using a marker
@hookspec
def register_news_provider(register):
    """
    Register a news provider.
    
    Args:
        register: A function that registers a news provider function
    """

@hookspec
def register_summarizer(register):
    """
    Register a summarization method.
    
    Args:
        register: A function that registers a summarization function
    """