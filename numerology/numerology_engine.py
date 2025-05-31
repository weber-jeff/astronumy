
from typing import Union, Dict
from datetime import datetime
import sys
import os
import json

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import reduce_number utility
from numerology.utils.reduction import reduce_number

# Pythagorean letter-to-number map
PYTHAGOREAN_MAP = {
    'A': 1, 'J': 1, 'S': 1,
    'B': 2, 'K': 2, 'T': 2,
    'C': 3, 'L': 3, 'U': 3,
    'D': 4, 'M': 4, 'V': 4,
    'E': 5, 'N': 5, 'W': 5,
    'F': 6, 'O': 6, 'X': 6,
    'G': 7, 'P': 7, 'Y': 7,
    'H': 8, 'Q': 8, 'Z': 8,
    'I': 9, 'R': 9
}

VOWELS = "AEIOU"

# ----------------------
# Utility Functions
# ----------------------

def clean_name(name: str) -> str:
    return "".join(name.upper().split())

# ----------------------
# Meaning Loader Class
# ----------------------

class NumerologyMeanings:
    def __init__(self, filepath: str):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.meanings = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Meanings file not found: {filepath}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in meanings file: {filepath}") from e

    def get(self, key: Union[int, str]) -> str:
        return self.meanings.get(str(key), f"Meaning not found for {key}.")

    def get_combination(self, key1: int, key2: int) -> str:
        combo_key = f"{key1}+{key2}"
        return self.meanings.get(combo_key, f"Combined meaning not found for {combo_key}.")

# ----------------------
# Numerology Engine
# ----------------------

class NumerologyEngine:
    def __init__(self, meanings: NumerologyMeanings):
        self.meanings = meanings

    def reduce(self, number: int, keep_master: bool = True) -> int:
        return reduce_number(number, keep_master)

    def letter_to_number(self, char: str) -> int:
        return PYTHAGOREAN_MAP.get(char.upper(), 0)

    def name_to_core(self, name: str) -> Dict[str, int]:
        cleaned_name = clean_name(name)
        expression = sum(self.letter_to_number(c) for c in cleaned_name)
        soul_urge = sum(self.letter_to_number(c) for c in cleaned_name if c in VOWELS)
        personality = sum(self.letter_to_number(c) for c in cleaned_name if c not in VOWELS)
        return {
            "Expression": self.reduce(expression),
            "Soul Urge": self.reduce(soul_urge),
            "Personality": self.reduce(personality)
        }

    def calculate_life_path(self, birth_date: Union[str, datetime]) -> int:
        if isinstance(birth_date, str):
            try:
                dt = datetime.strptime(birth_date, "%Y-%m-%d")
            except Exception as e:
                raise ValueError("Birth date must be 'YYYY-MM-DD' or datetime object") from e
        elif isinstance(birth_date, datetime):
            dt = birth_date
        else:
            raise TypeError("birth_date must be str or datetime")

        month_reduced = self.reduce(dt.month)
        day_reduced = self.reduce(dt.day)
        year_sum_digits = sum(int(d) for d in str(dt.year))
        year_reduced = self.reduce(year_sum_digits)
        return self.reduce(month_reduced + day_reduced + year_reduced)

    def generate_report(self, birth_date: Union[str, datetime], full_name: str) -> Dict[str, Dict]:
        life_path = self.calculate_life_path(birth_date)
        core = self.name_to_core(full_name)

        # Placeholder logic for future expansion (use actual logic later)
        maturity = self.reduce(life_path + core["Expression"])
        balance = self.reduce(abs(core["Soul Urge"] - core["Personality"]))
        hidden_passion = 7  # Replace with real logic
        challenge = 2       # Replace with real logic
        karmic = 13         # Replace with real logic
        pinnacle = 5        # Replace with real logic or import generator

        core_numbers = {
            "Life Path": life_path,
            "Expression": core["Expression"],
            "Soul Urge": core["Soul Urge"],
            "Personality": core["Personality"],
            "Maturity": maturity,
            "Balance": balance,
            "Hidden Passion": hidden_passion,
            "Challenge": challenge,
            "Karmic": karmic,
            "Pinnacle": pinnacle,
        }

        meanings = {
            key: self.meanings.get(value)
            for key, value in core_numbers.items()
        }

        # Add combinations
        meanings["Combinations"] = {
            "Life Path + Expression": self.meanings.get_combination(life_path, core["Expression"]),
            "Soul Urge + Personality": self.meanings.get_combination(core["Soul Urge"], core["Personality"])
        }

        return {
            "CoreNumbers": core_numbers,
            "Meanings": meanings
        }

# ----------------------
# Script Test Entry Point
# ----------------------

if __name__ == "__main__":
    test_meanings_file = os.path.join(os.path.dirname(__file__), "data", "life_path_meanings.json")
    meanings = NumerologyMeanings(test_meanings_file)
    engine = NumerologyEngine(meanings)
    report = engine.generate_report("1987-05-08", "Jeffery Allen Louis Weber")
    print(json.dumps(report, indent=2))
