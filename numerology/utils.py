import os
import json

def get_project_root() -> str:
    """
    Returns the absolute path to the project root.
    Adjust this based on where utils.py is located.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_data_dir(subfolder_name="data") -> str:
    """
    Returns the absolute path to the main JSON meanings directory.
    Default subfolder is 'data'.
    """
    return os.path.join(get_project_root(), subfolder_name)

def load_json_file(filepath: str) -> dict:
    """
    Load and return the contents of a JSON file as a dictionary.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in file {filepath}: {e}")

def safe_get(data: dict, key: str, default=None):
    """
    Safely retrieve a value from a dictionary with an optional fallback default.
    """
    return data.get(key, default)
