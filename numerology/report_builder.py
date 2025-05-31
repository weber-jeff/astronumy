import json
import os
from user_profile import UserProfile
from numerology.in_core_numerology import (
    life_path_report as life_path,
    soul_urge,
    expression,
    personality,
    balance,
    birthday,
    maturity,
    hidden_passion,
    karmic,
    pinnacle,
    personal,
    challenge
)

MEANINGS = {}

def preload_meanings():
    """Preload all numerology meanings into memory."""
    base_path = "numerology/meanings"
    for filename in os.listdir(base_path):
        if filename.endswith(".json"):
            category = filename.replace("_meanings.json", "")
            full_path = os.path.join(base_path, filename)
            try:
                with open(full_path, "r") as f:
                    MEANINGS[category] = json.load(f)
            except Exception as e:
                MEANINGS[category] = {"error": f"Failed to load: {e}"}

def get_meaning(category: str, key: int | str) -> dict:
    """Safely retrieve a meaning from preloaded MEANINGS."""
    data = MEANINGS.get(category, {})
    meaning = data.get(str(key), "Meaning not found.")
    return {
        "value": key,
        "meaning": meaning,
        "source": category
    }

def generate_numerology_report(user: UserProfile) -> dict:
    """Generate a complete numerology report for a given user."""
    report = {
        "name": user.name,
        "birthdate": user.birthdate.isoformat(),
        "core_numbers": {},
        "karmic_insights": {},
        "life_cycles": {},
    }

    # === CORE NUMBERS ===
    lp = life_path.calculate(user.birth_day, user.birth_month, user.birth_year)
    exp = expression.calculate(user.name)
    su = soul_urge.calculate(user.name)
    per = personality.calculate(user.name)
    bd = birthday.calculate(user.birth_day)
    mat = maturity.calculate(lp, exp)
    bal = balance.calculate(user.name)
    hp = hidden_passion.calculate(user.name)

    report["core_numbers"] = {
        "Life Path": get_meaning("life_path", lp),
        "Expression": get_meaning("expression", exp),
        "Soul Urge": get_meaning("soul_urge", su),
        "Personality": get_meaning("personality", per),
        "Birthday": get_meaning("birthday", bd),
        "Maturity": get_meaning("maturity", mat),
        "Balance": get_meaning("balance", bal),
        "Hidden Passion": get_meaning("hidden_passion", hp),
    }

    # === CHALLENGES ===
    ch1, ch2, ch3 = challenge.calculate(user.birth_day, user.birth_month, user.birth_year)
    report["karmic_insights"]["Challenges"] = {
        "Challenge 1": get_meaning("challenge", ch1),
        "Challenge 2": get_meaning("challenge", ch2),
        "Challenge 3": get_meaning("challenge", ch3),
    }

    # === KARMIC LESSONS ===
    karmics = karmic.calculate(user.name)
    report["karmic_insights"]["Karmic Lessons"] = [
        get_meaning("karmic", k) for k in karmics
    ]

    # === PINNACLES ===
    p1, p2, p3, p4 = pinnacle.calculate(user.birth_day, user.birth_month, user.birth_year)
    report["life_cycles"]["Pinnacles"] = {
        "Pinnacle 1": get_meaning("pinnacle", p1),
        "Pinnacle 2": get_meaning("pinnacle", p2),
        "Pinnacle 3": get_meaning("pinnacle", p3),
        "Pinnacle 4": get_meaning("pinnacle", p4),
    }

    return report
