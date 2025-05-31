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
data = load_meaning("planet_sign_meanings")
venus_in_leo = data["Venus"]["Leo"]
mars_in_capricorn = data["Mars"]["Capricorn"]
data = load_meaning("jupiter_saturn_sign_meanings")
jupiter_in_gemini = data["Jupiter"]["Gemini"]
saturn_in_virgo = data["Saturn"]["Virgo"]
data = load_meaning("uranus_neptune_sign_meanings")
uranus_aquarius = data["Uranus"]["Aquarius"]
neptune_pisces = data["Neptune"]["Pisces"]
pluto_data = load_meaning("pluto_sign_meanings")
pluto_in_virgo = pluto_data["Pluto"]["Virgo"]
