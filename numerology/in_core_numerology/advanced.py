import json
import os
from numerology.in_core_numerology.pinnacle import calculate_pinnacle_numbers
from numerology.numerology_engine import reduce_number
# Get the directory where this script resides
base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, "advanced_meanings.json")

# Load meanings JSON
with open(json_path, "r") as f:
    meanings = json.load(f)



def get_combined_meanings(life_path, expression, soul_urge, personality, maturity, birthday, balance, challenge, birth_date_str, meanings,pinnacle1, pinnacle2, pinnacle3, pinnacle4):
    results = {}
    
    pinnacles = calculate_pinnacle_numbers(birth_date_str)  # returns [p1, p2, p3, p4]

    if any(isinstance(p, str) for p in pinnacles):
        print("Error calculating pinnacles:", pinnacles)
        return {}

    pinnacle1, pinnacle2, pinnacle3, pinnacle4 = pinnacles

    combined_values = {
        "Pinnacle1 + Pinnacle2": pinnacle1 + pinnacle2,
        "Expression + Challenge": expression + challenge,
        "Soul Urge + Pinnacle": soul_urge + maturity,
        "Life Path + Challenge": life_path + challenge,
        "Expression + Personality": expression + personality,
        "Life Path + Soul Urge": life_path + soul_urge,
        "Life Path + Expression": life_path + expression,
        "Soul Urge + Personality": soul_urge + personality,
        "Life Path + Maturity": life_path + maturity,
        "Birthday + Balance": birthday + balance,
        "Expression + Soul Urge + Personality": expression + soul_urge + personality,
    }

    for key, total in combined_values.items():  # Fixed `combos` to `combined_values`
        reduced_num = reduce_number(total)
        key_str = str(reduced_num)
        meaning = meanings.get(key, {}).get(key_str, "Meaning not found")
        results[key] = {"number": reduced_num, "meaning": meaning}

    return results

# --- Example usage ---
life_path = 7
expression = 4
soul_urge = 9
personality = 3
maturity = 6
birthday = 2
balance = 1
challenge = 5
birth_date_str = "1987-05-08"  # YYYY-MM-DD format

results = get_combined_meanings(
    life_path, expression, soul_urge, personality,
    maturity, birthday, balance, challenge, birth_date_str, meanings, pinnacle1=None, pinnacle2=None, pinnacle3=None, pinnacle4=None
)

for combo, data in results.items():
    print(f"{combo}: Number = {data['number']}")
    print(f"Meaning: {data['meaning']}\n")

print("Current Working Directory:", os.getcwd())
