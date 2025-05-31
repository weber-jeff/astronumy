import os
import json

def load_meaning(name):
    """
    Loads a JSON-formatted meanings file from astrology/json/ folder.

    Args:
        name (str): Name of the JSON file without the .json extension

    Returns:
        dict: Parsed dictionary from the JSON file
    """
    base_dir = os.path.dirname(__file__)
    # Corrected path: The 'json' directory is directly under 'base_dir'
    json_dir = os.path.join(base_dir, "json")
    json_path = os.path.join(json_dir, f"{name}.json")

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise ImportError(f"[load_meaning] Could not find JSON file: {json_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"[load_meaning] Error parsing {json_path}: {e}")

if __name__ == "__main__":
    # This block will only run when the script is executed directly
    # For testing or example usage
    print("Testing load_meaning function...")
    planet_sign_data = load_meaning("planet_sign_meanings")
    print(f"Venus in Leo: {planet_sign_data.get('Venus', {}).get('Leo', 'Not found')}")
    print(f"Mars in Capricorn: {planet_sign_data.get('Mars', {}).get('Capricorn', 'Not found')}")

    jupiter_saturn_data = load_meaning("jupiter_saturn_sign_meanings")
    print(f"Jupiter in Gemini: {jupiter_saturn_data.get('Jupiter', {}).get('Gemini', 'Not found')}")

    # Add other test loads as needed
    print("Test loading complete.")
