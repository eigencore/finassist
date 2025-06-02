import os

def get_env_var(var_name: str) -> str:
    """Get environment variable with error handling."""
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"Environment variable {var_name} is not set")
    return value