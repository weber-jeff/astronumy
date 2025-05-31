
import json
import os
from numerology.numerology_engine import PYTHAGOREAN_MAP

json_path = os.path.join(os.path.dirname(__file__), 'karmic_meanings.json')

with open(json_path, 'r', encoding='utf-8') as f:
    karmic_meanings = json.load(f)


def calculate_karmic_lesson_number(full_name_str: str) -> int | str:
    """Calculates the Karmic Lesson number from the name."""
    try:
        name_for_calc = "".join(filter(str.isalpha, full_name_str)).upper()
        if not name_for_calc: return "Name Required for Karmic Lesson"
        present_digits = {PYTHAGOREAN_MAP[char] for char in name_for_calc if char in PYTHAGOREAN_MAP}
        for i in range(1, 10): # Check for missing digits 1 through 9
            if i not in present_digits:
                return i
        return 0  # All digits 1-9 are present
    except Exception as e: return f"Error calculating Karmic Lesson: {e}"

def get_karmic_analysis(number: int) -> dict:
    meaning = karmic_meanings.get(str(number))
    if not meaning:
        return {
            "summary": "Invalid Karmic  number. Please enter a valid number.",
            "advice": None,
            "master": False,
            "element": None,
            "traits": [],
            "strengths": [],
            "weaknesses": [],
            "business": None,
            "relationships": None,
            "purpose": None,
            "vibration": None,
            "color": None,
        }
    return {
        "summary": f"Karmic Lesson {number} - {meaning['description']}",
        "advice": meaning.get("advice"),
        "master": meaning.get("master", False),
        "element": meaning.get("element"),
        "traits": meaning.get("traits", []),
        "strengths": meaning.get("strengths", []),
        "weaknesses": meaning.get("weaknesses", []),
        "business": meaning.get("business"),
        "relationships": meaning.get("relationships"),
        "purpose": meaning.get("purpose"),
        "vibration": meaning.get("vibration"),
        "color": meaning.get("color"),
    }

def get_karmic_report_string(number: int) -> str:
    analysis = get_karmic_analysis(number)
    lines = [
        "=" * 60,
        f"⚖️ Karmic Lesson {number} Report ⚖️",
        "=" * 60,
        f"🧾 Summary: {analysis['summary']}",
    ]

    if analysis["advice"]:
        lines.append(f"💡 Advice: {analysis['advice']}")
        lines.append(f"✨ Master Number: {'Yes' if analysis['master'] else 'No'}")
        lines.append(f"🜂 Element: {analysis['element']}")
        lines.append(f"🎨 Color: {analysis['color']}")
        lines.append(f"🔮 Vibration: {analysis['vibration']}\n")

        lines.append("🔑 Core Traits: " + ', '.join(analysis["traits"]))
        lines.append("✅ Strengths: " + ', '.join(analysis["strengths"]))
        lines.append("⚠️ Weaknesses: " + ', '.join(analysis["weaknesses"]))

        lines.append("\n💼 Business Outlook:")
        lines.append(f" - {analysis['business']}")

        lines.append("\n❤️ Relationships:")
        lines.append(f" - {analysis['relationships']}")

        lines.append("\n🎯 Life Purpose:")
        lines.append(f" - {analysis['purpose']}")

    lines.append("=" * 60)
    return "\n".join(lines)

if __name__ == "__main__":
    test_num = 1
    print(get_karmic_report_string(test_num))
