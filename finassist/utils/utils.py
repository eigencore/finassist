import os

def get_var_env(var_name: str) -> str:
    """
    Get the value of an environment variable.
    
    Args:
        var_name (str): The name of the environment variable.
    
    Returns:
        str: The value of the environment variable, or None if not set.
    """
    var = os.getenv(var_name, None)
    if var is None:
        raise ValueError(f"Environment variable '{var_name}' is not set.")
    return var