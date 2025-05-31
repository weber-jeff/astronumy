import json
import os
from datetime import datetime

# Corrected path to point to the 'data' directory, which is one level up
json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'life_path_meanings.json')

with open(json_path, 'r', encoding='utf-8') as f:
    life_path_meanings = json.load(f)


def sum_digits(n: int) -> int:
    while n > 9:
        n = sum(int(digit) for digit in str(n))
    return n


    year_sum = sum_digits(birth_date.year)
    month_sum = sum_digits(birth_date.month)
    day_sum = sum_digits(birth_date.day)

    life_path = sum_digits(year_sum + month_sum + day_sum)
    return life_path
def calculate_life_path(birth_date_str: str) -> int:
    try:
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return 0

    year_sum = sum_digits(birth_date.year)
    month_sum = sum_digits(birth_date.month)
    day_sum = sum_digits(birth_date.day)

    total = year_sum + month_sum + day_sum

    if total in (11, 22, 33):
        return total

    return sum_digits(total)
                                                                         

def get_life_path_analysis(number: int) -> dict:
    meaning = life_path_meanings.get(str(number))
    if not meaning:
        return {
            "summary": "Invalid Life Path number. Please enter a valid number.",
            "advice": None,
            "master": False,
            "element": None,
            "color": None,
            "vibration": None,
            "traits": [],
            "strengths": [],
            "weaknesses": [],
            "business": None,
            "relationships": None,
            "purpose": None,
        }
    return {
        "summary": f"Life Path {number} - {meaning['description']}",
        "advice": meaning.get('advice'),
        "master": meaning.get('master', False),
        "element": meaning.get('element'),
        "color": meaning.get('color'),
        "vibration": meaning.get('vibration'),
        "traits": meaning.get('traits', []),
        "strengths": meaning.get('strengths', []),
        "weaknesses": meaning.get('weaknesses', []),
        "business": meaning.get('business'),
        "relationships": meaning.get('relationships'),
        "purpose": meaning.get('purpose'),
    }


def get_life_path_report_string(number: int) -> str:
    analysis = get_life_path_analysis(number)

    lines = [
        "=" * 60,
        f"🌟 Life Path {number} Report 🌟",
        "=" * 60,
        f"🧾 Summary: {analysis['summary']}",
    ]

    # Always print these fields if available, regardless of advice
    if analysis['advice']:
        lines.append(f"💡 Advice: {analysis['advice']}")

    lines.append(f"✨ Master Number: {'Yes' if analysis['master'] else 'No'}")
    lines.append(f"🜂 Element: {analysis['element']}")
    lines.append(f"🎨 Color: {analysis['color']}")
    lines.append(f"🔮 Vibration: {analysis['vibration']}\n")

    if analysis['traits']:
        lines.append("🔑 Core Traits: " + ', '.join(analysis['traits']))
    if analysis['strengths']:
        lines.append("✅ Strengths: " + ', '.join(analysis['strengths']))
    if analysis['weaknesses']:
        lines.append("⚠️ Weaknesses: " + ', '.join(analysis['weaknesses']))

    if analysis['business']:
        lines.append("\n💼 Business Outlook:")
        lines.append(f" - {analysis['business']}")

    if analysis['relationships']:
        lines.append("\n❤️ Relationships:")
        lines.append(f" - {analysis['relationships']}")

    if analysis['purpose']:
        lines.append("\n🎯 Life Purpose:")
        lines.append(f" - {analysis['purpose']}")

    lines.append("=" * 60)
    return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    test_number = 2  # Change this number to test other Life Path numbers
    print(get_life_path_report_string(test_number))
