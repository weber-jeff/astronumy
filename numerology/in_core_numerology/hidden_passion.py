import json
import os
from numerology.numerology_engine import reduce_number, PYTHAGOREAN_MAP,Counter
# Load the hidden passion meanings JSON


json_path = os.path.join(os.path.dirname(__file__), 'hidden_passion_meanings.json')
with open(json_path, 'r', encoding='utf-8') as f:
    hidden_passion_meanings = json.load(f)


def calculate_hidden_passion_number(full_name_str: str) -> int | str:
    """Calculates the Hidden Passion number (sum of most frequent digits, reduced)."""
    try:
        name_for_calc = "".join(filter(str.isalpha, full_name_str)).upper()
        if not name_for_calc: return "Name Required"

        all_digits_in_name = [PYTHAGOREAN_MAP[char] for char in name_for_calc if char in PYTHAGOREAN_MAP]
        if not all_digits_in_name: return "No valid letters for Hidden Passion calculation"

        digit_counts = Counter(all_digits_in_name)
        if not digit_counts: return "No digits found in name for Hidden Passion"

        max_freq = max(digit_counts.values())
        most_frequent_digits = [num for num, count in digit_counts.items() if count == max_freq]

        if not most_frequent_digits:
            return "No dominant digit found for Hidden Passion"
        
        hidden_passion_sum = sum(most_frequent_digits)
        return reduce_number(hidden_passion_sum)
    except Exception as e: return f"Error calculating Hidden Passion: {e}"
    

def get_hidden_passion_analysis(number: int) -> dict:
    """Return the hidden passion meaning for a given number."""
    meaning = hidden_passion_meanings.get(str(number))
    if not meaning:
        return {
            "summary": "Invalid Hidden Passion number. Please enter a valid number.",
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
        "summary": f"Hidden Passion {number} - {meaning['description']}",
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

def get_hidden_passion_report_string(number: int) -> str:
    """Generate a formatted hidden passion report string."""
    analysis = get_hidden_passion_analysis(number)
    report_lines = [
        "=" * 60,
        f"🎯 Hidden Passion {number} Report 🎯",
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

if __name__ == "__main__":
    test_number = 7  # Replace with any number you want to test
    print(get_hidden_passion_report_string(test_number))
