import json
import os
from numerology.numerology_engine import reduce_number


def load_meanings(filename: str) -> dict:
    """Load JSON meanings from the data folder."""
    json_path = os.path.join(os.path.dirname(__file__), filename)
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def calculate_maturity_number(life_path_num: int, expression_num: int) -> int | str:
    """
    Calculates the Maturity Number by summing Life Path and Expression numbers,
    preserving master numbers (11, 22, 33).
    """
    if not (isinstance(life_path_num, int) and isinstance(expression_num, int)):
        return "Valid Life Path and Expression numbers required"
    maturity_sum = life_path_num + expression_num
    return reduce_number(maturity_sum, preserve_master=True)


def get_maturity_analysis(number: int) -> dict:
    """Get the maturity number meaning from the JSON."""
    meanings = load_meanings('maturity_meanings.json')
    meaning = meanings.get(str(number))
    
    # Default return if number not in meanings
    if not meaning:
        return {
            "summary": f"Invalid Maturity Number. Please enter a valid number.",
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

    # Return structured dictionary with fallback defaults
    return {
        "summary": f"Maturity {number} – {meaning.get('description', 'No description provided.')}",
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


def get_maturity_report_string(number: int) -> str:
    """
    Generate a well-formatted string report for the given maturity number.
    Always includes all available sections, even if some values are missing.
    """
    analysis = get_maturity_analysis(number)
    report_lines = [
        "=" * 60,
        f"🌟 Maturity {number} Report 🌟",
        "=" * 60,
        f"🧾 Summary: {analysis['summary']}",
        f"💡 Advice: {analysis['advice'] or 'N/A'}",
        f"✨ Master Number: {'Yes' if analysis['master'] else 'No'}",
        f"🜂 Element: {analysis['element'] or 'N/A'}",
        f"🎨 Color: {analysis['color'] or 'N/A'}",
        f"🔮 Vibrations: {analysis['vibrations'] or 'N/A'}\n",
        "🔑 Core Traits: " + ', '.join(analysis['traits'] or ['N/A']),
        "✅ Strengths: " + ', '.join(analysis['strengths'] or ['N/A']),
        "⚠️ Weaknesses: " + ', '.join(analysis['weaknesses'] or ['N/A']),
        "\n💼 Business Outlook:",
        f" - {analysis['business'] or 'N/A'}",
        "\n❤️ Relationships:",
        f" - {analysis['relationships'] or 'N/A'}",
        "\n🎯 Life Purpose:",
        f" - {analysis['purpose'] or 'N/A'}",
        "=" * 60
    ]
    return "\n".join(report_lines)


# Optional dual output interface
def get_maturity_report(number: int, as_string: bool = True) -> str | dict:
    """Return either a formatted string report or raw analysis dictionary."""
    return get_maturity_report_string(number) if as_string else get_maturity_analysis(number)


# Example usage for testing
if __name__ == "__main__":
    test_life_path = 9
    test_expression = 4
    maturity = calculate_maturity_number(test_life_path, test_expression)
    print(get_maturity_report(maturity, as_string=True))
