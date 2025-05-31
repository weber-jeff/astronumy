import json
import os
from numerology.numerology_engine import reduce_number
from birthday import get_reduced_date_components
from typing import  Union, List # Keep one import for typing if needed elsewhere
from datetime import datetime

def validate_date_format(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def calculate_challenge_numbers(birth_date_str: str) -> Union[List[int], str]:
    if not validate_date_format(birth_date_str):
        return "Invalid date format, expected YYYY-MM-DD"
    # existing logic follows ...

json_path = os.path.join(os.path.dirname(__file__), 'challenge_meanings.json')
with open(json_path, 'r', encoding='utf-8') as f:
    challenge_meanings = json.load(f)
def calculate_challenge_numbers(birth_date_str: str) -> list[int | str] | str:
    components = get_reduced_date_components(birth_date_str)
    if isinstance(components, str): return f"Cannot calculate Challenges: {components}"
    r_month, r_day, r_year = components
    sd_month = reduce_number(r_month, keep_master_as_is=False)
    sd_day = reduce_number(r_day, keep_master_as_is=False)
    sd_year = reduce_number(r_year, keep_master_as_is=False)
    if not all(isinstance(i, int) for i in [sd_month, sd_day, sd_year]):
         return "Invalid date components for Challenges after reduction."
    try:
        challenge1 = reduce_number(abs(sd_month - sd_day), keep_master_as_is=False)
        challenge2 = reduce_number(abs(sd_day - sd_year), keep_master_as_is=False)
        main_challenge3 = reduce_number(abs(challenge1 - challenge2), keep_master_as_is=False)
        challenge4 = reduce_number(abs(sd_month - sd_year), keep_master_as_is=False)
        return [challenge1, challenge2, main_challenge3, challenge4]
    except Exception as e: return f"Error calculating Challenges: {e}"

def get_challenge_analysis(challenge_num: int) -> dict:
    """Return challenge meaning for a given challenge number."""
    meaning = challenge_meanings.get(str(challenge_num))
    if not meaning:
        return {
            "summary": "Invalid Challenge Number. Please enter a valid challenge number.",
            "advice": None,
            "master": False,
            "element": None,
            "traits": [],
            "strengths": [],
            "weaknesses": [],
            "business": None,
            "relationships": None,
            "purpose": None,
            "color": None,
            "vibration": None,
        }

    return {
        "summary": f"Challenge {challenge_num} - {meaning['description']}",
        "advice": meaning.get('advice'),
        "master": meaning.get('master', False),
        "element": meaning.get('element'),
        "traits": meaning.get('traits', []),
        "strengths": meaning.get('strengths', []),
        "weaknesses": meaning.get('weaknesses', []),
        "business": meaning.get('business'),
        "relationships": meaning.get('relationships'),
        "purpose": meaning.get('purpose'),
        "color": meaning.get('color'),
        "vibration": meaning.get('vibration'),
    }

def get_challenge_report_string(challenge_num: int) -> str:
    """Generate formatted Challenge report string."""
    analysis = get_challenge_analysis(challenge_num)
    report_lines = [
        "=" * 60,
        f"⚔️ Challenge {challenge_num} Report ⚔️",
        "=" * 60,
        f"🧾 Summary: {analysis['summary']}"
    ]

    if analysis['advice']:
        report_lines.append(f"💡 Advice: {analysis['advice']}")
        report_lines.append(f"✨ Master Number: {'Yes' if analysis['master'] else 'No'}")
        report_lines.append(f"🜂 Element: {analysis['element']}")
        report_lines.append(f"🎨 Color: {analysis['color']}")
        report_lines.append(f"🔮 Vibration: {analysis['vibration']}\n")

        report_lines.append("🔑 Core Traits: " + ', '.join(analysis['traits']))
        report_lines.append("✅ Strengths: " + ', '.join(analysis['strengths']))
        report_lines.append("⚠️ Weaknesses: " + ', '.join(analysis['weaknesses']))

        report_lines.append("\n💼 Business Outlook:")
        report_lines.append(f" - {analysis['business']}")

        report_lines.append("\n❤️ Relationships:")
        report_lines.append(f" - {analysis['relationships']}")

        report_lines.append("\n🎯 Life Purpose:")
        report_lines.append(f" - {analysis['purpose']}")

    report_lines.append("=" * 60)

    return "\n".join(report_lines)

# Example quick test block
if __name__ == "__main__":
    test_challenge_num = 3
    print(get_challenge_report_string(test_challenge_num))
