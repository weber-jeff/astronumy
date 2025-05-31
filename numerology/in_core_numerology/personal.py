import json
import os
from datetime import datetime
from numerology.numerology_engine import reduce_number

# Load Personal Cycle meanings JSON
json_path = os.path.join(os.path.dirname(__file__), 'personal_meanings.json')
with open(json_path, 'r', encoding='utf-8') as f:
    personal_meanings = json.load(f)


def calculate_personal_cycles(birth_month: int, birth_day: int, birth_year: int,
                              target_year: int, target_month: int, target_day: int) -> dict:
    """
    Calculate Personal Year, Month, and Day numbers.
    """
    birth_sum = reduce_number(birth_month + birth_day)
    year_sum = reduce_number(sum(int(d) for d in str(target_year)))
    personal_year = reduce_number(birth_sum + year_sum)
    personal_month = reduce_number(personal_year + target_month)
    personal_day = reduce_number(personal_month + target_day)

    return {
        "Personal Year": personal_year,
        "Personal Month": personal_month,
        "Personal Day": personal_day
    }


def get_numerological_insights(birth_month: int, birth_day: int, target_date_obj: datetime) -> dict:
    """
    Get a simple snapshot of personal day/month/year using a direct date.
    """
    try:
        personal_day = reduce_number(birth_month + birth_day + target_date_obj.day)
        personal_month = reduce_number(birth_month + target_date_obj.month)
        personal_year = reduce_number(birth_month + birth_day + target_date_obj.year)
        return {
            "personal_day": f"{personal_day} – Energy of {personal_day}. Themes TBD",
            "personal_month": str(personal_month),
            "personal_year": str(personal_year),
        }
    except Exception as e:
        return {"error": "Failed to calculate numerological insights", "details": str(e)}


def get_personal_analysis(number: int) -> dict:
    """
    Fetch meaning data from JSON for a given Personal number.
    """
    meaning = personal_meanings.get(str(number))
    if not meaning:
        return {
            "summary": f"Invalid Personal Cycle number {number}.",
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
        "summary": f"Personal Cycle {number} – {meaning.get('description', 'No description provided.')}",
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


def get_personal_report_string(number: int) -> str:
    """
    Build a formatted Personal Cycle report as a string.
    """
    analysis = get_personal_analysis(number)
    report_lines = [
        "=" * 60,
        f"🔄 Personal Cycle {number} Report 🔄",
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


def get_personal_report(number: int, as_string: bool = True) -> str | dict:
    """
    Unified interface to get either a raw dictionary or string report.
    """
    return get_personal_report_string(number) if as_string else get_personal_analysis(number)


# Standalone test execution
if __name__ == "__main__":
    test_number = 7  # Example test number
    print(get_personal_report(test_number, as_string=True))
