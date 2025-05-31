import os
import json
from typing import Union, List
from numerology.utils.reduction import reduce_number
# Corrected import to be an explicit relative import
from .birthday import get_reduced_date_components

# Load Pinnacle meanings JSON once at module load
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, '..', 'data', 'pinnacle_meanings.json') # Corrected path

def load_pinnacle_meanings(json_path=JSON_PATH) -> dict[int, dict]:
    """Load and return the pinnacle meanings dictionary from JSON."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return {int(k): v for k, v in data.items()}

pinnacle_meanings = load_pinnacle_meanings()

def calculate_pinnacle_numbers(birth_date_str: str) -> List[Union[int, str]]:
    """
    Calculate the 4 Pinnacle numbers from birth date string (YYYY-MM-DD).
    Returns list of 4 numbers or error messages.
    """
    components = get_reduced_date_components(birth_date_str)
    if isinstance(components, str):
        return [f"Error: {components}"] * 4

    r_month, r_day, r_year = components
    if not all(isinstance(i, int) for i in (r_month, r_day, r_year)):
        return ["Invalid date components."] * 4

    try:
        pinnacle1 = reduce_number(r_month + r_day)
        pinnacle2 = reduce_number(r_day + r_year)
        pinnacle3 = reduce_number(pinnacle1 + pinnacle2)
        pinnacle4 = reduce_number(r_month + r_year)
        return [pinnacle1, pinnacle2, pinnacle3, pinnacle4]
    except Exception as e:
        return [f"Calculation error: {e}"] * 4

def get_pinnacle_analysis(number: int) -> dict:
    default = {
        "summary": "Invalid Pinnacle number.",
        "advice": "Please provide a valid Pinnacle number (1-9, 11, 22, 33).",
        "master": False,
        "traits": [],
        "strengths": [],
        "weaknesses": [],
        "business": None,
        "relationships": None,
        "purpose": None,
        "color": None,
        "vibrations": None,
    }
    meaning = pinnacle_meanings.get(number, default)
    return {
        "summary": meaning.get("description", default["summary"]),
        "advice": meaning.get("advice", default["advice"]),
        "master": meaning.get("master", default["master"]),
        "traits": meaning.get("traits", default["traits"]),
        "strengths": meaning.get("strengths", default["strengths"]),
        "weaknesses": meaning.get("weaknesses", default["weaknesses"]),
        "business": meaning.get("business", default["business"]),
        "relationships": meaning.get("relationships", default["relationships"]),
        "purpose": meaning.get("purpose", default["purpose"]),
        "color": meaning.get("color", default["color"]),
        "vibrations": meaning.get("vibrations", default["vibrations"]),
    }

def generate_pinnacle_report(birth_date_str: str) -> dict:
    """
    Generate a full report dictionary containing pinnacle numbers and their meanings.
    """
    pinnacles = calculate_pinnacle_numbers(birth_date_str)
    if any(isinstance(n, str) and n.startswith("Error") for n in pinnacles):
        return {"error": pinnacles[0]}

    report = {}
    for i, num in enumerate(pinnacles, start=1):
        report[f"pinnacle{i}"] = {
            "number": num,
            "meaning": get_pinnacle_analysis(num)
        }
    return report

def format_pinnacle_report(report: dict) -> str:
    if "error" in report:
        return f"Error generating report: {report['error']}"

    lines = ["=" * 60, "🌟 Pinnacle Report 🌟", "=" * 60]
    for i in range(1, 5):
        p = report.get(f"pinnacle{i}")
        if not p:
            continue
        num = p["number"]
        m = p["meaning"]
        lines.append(f"\nPinnacle {i} (Number {num}):")
        lines.append(f"Summary: {m['summary']}")
        lines.append(f"Advice: {m['advice']}")
        lines.append(f"Master Number: {'Yes' if m['master'] else 'No'}")
        lines.append(f"Traits: {', '.join(m['traits'])}")
        lines.append(f"Strengths: {', '.join(m['strengths'])}")
        lines.append(f"Weaknesses: {', '.join(m['weaknesses'])}")
        lines.append(f"Business: {m['business']}")
        lines.append(f"Relationships: {m['relationships']}")
        lines.append(f"Purpose: {m['purpose']}")
        lines.append(f"Color: {m['color']}")
        lines.append(f"Vibrations: {m['vibrations']}")
        lines.append("-" * 60)
    return "\n".join(lines)


# CLI example for quick test
if __name__ == "__main__":
    import sys
    birth_date = sys.argv[1] if len(sys.argv) > 1 else "1987-05-08"
    report = generate_pinnacle_report(birth_date)
    print(format_pinnacle_report(report))
