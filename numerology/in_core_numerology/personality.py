# personality.py - Module for calculating and analyzing the Personality number

import os
import json
import unicodedata
from numerology.numerology_engine import get_number_from_string, reduce_number, PYTHAGOREAN_MAP, VOWELS

# Load Personality meanings JSON
json_path = os.path.join(os.path.dirname(__file__), 'personality_meanings.json')
with open(json_path, 'r', encoding='utf-8') as f:
    personality_meanings = json.load(f)


def normalize_name(name: str) -> str:
    """Normalize accented characters and remove non-alpha characters."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', name)
        if unicodedata.category(c) != 'Mn' and c.isalpha()
    )


def calculate_personality_number(full_name_str: str) -> int:
    """Calculates the Personality number from consonants in the full name."""
    try:
        normalized = normalize_name(full_name_str)
        consonant_str = ''.join(char for char in normalized.upper() if char not in VOWELS)
        if not consonant_str:
            return 0  # No consonants found
        consonant_sum = get_number_from_string(consonant_str, PYTHAGOREAN_MAP)
        return reduce_number(consonant_sum)
    except Exception as e:
        print(f"Error in calculate_personality_number: {e}")
        return "Error"


def get_personality_analysis(number: int) -> dict:
    """Return the personality meaning for a given number."""
    meaning = personality_meanings.get(str(number))
    if not meaning:
        return {
            "summary": "Invalid Personality number.",
            "advice": None,
            "master": False,
            "element": None,
            "color": None,
            "vibrations": None,
            "traits": [],
            "strengths": [],
            "weaknesses": [],
            "business": None,
            "relationships": None,
            "purpose": None,
        }

    return {
        "summary": f"Personality {number} - {meaning['description']}",
        "advice": meaning.get('advice'),
        "master": meaning.get('master', False),
        "element": meaning.get('element'),
        "color": meaning.get('color'),
        "vibrations": meaning.get('vibrations'),
        "traits": meaning.get('traits', []),
        "strengths": meaning.get('strengths', []),
        "weaknesses": meaning.get('weaknesses', []),
        "business": meaning.get('business'),
        "relationships": meaning.get('relationships'),
        "purpose": meaning.get('purpose'),
    }


def get_personality_report_string(number: int) -> str:
    """Generates a styled report string for a Personality number."""
    analysis = get_personality_analysis(number)
    lines = [
        "=" * 60,
        f"🎭 Personality {number} Report 🎭",
        "=" * 60,
        f"🧾 Summary: {analysis['summary']}"
    ]

    if analysis['advice']:
        lines.append(f"💡 Advice: {analysis['advice']}")
        lines.append(f"✨ Master Number: {'Yes' if analysis['master'] else 'No'}")
        lines.append(f"🜂 Element: {analysis['element']}")
        lines.append(f"🎨 Color: {analysis['color']}")
        lines.append(f"🔮 Vibrations: {analysis['vibrations']}\n")

        lines.append("🔑 Core Traits: " + ', '.join(analysis['traits']))
        lines.append("✅ Strengths: " + ', '.join(analysis['strengths']))
        lines.append("⚠️ Weaknesses: " + ', '.join(analysis['weaknesses']))

        lines.append("\n💼 Business Outlook:")
        lines.append(f" - {analysis['business']}")

        lines.append("\n❤️ Relationships:")
        lines.append(f" - {analysis['relationships']}")

        lines.append("\n🎯 Life Purpose:")
        lines.append(f" - {analysis['purpose']}")

    lines.append("=" * 60)
    return "\n".join(lines)


# Example test execution
if __name__ == "__main__":
    full_name = "Elon Musk"
    personality_number = calculate_personality_number(full_name)
    print(get_personality_report_string(personality_number))
