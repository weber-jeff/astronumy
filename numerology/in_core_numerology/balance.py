import json
import os
from typing import Union

# Optional: caching loaded JSON so file loads only once
_meanings_cache = None

def _load_meanings() -> dict:
    global _meanings_cache
    if _meanings_cache is not None:
        return _meanings_cache

    # Build path to JSON meanings file relative to this script
    current_dir = os.path.dirname(__file__)
    json_path = os.path.join(current_dir, '..', '..', 'data', 'balance_meaning.json')

    with open(json_path, 'r', encoding='utf-8') as f:
        _meanings_cache = json.load(f)
    return _meanings_cache


def calculate_balance_number(full_name: str) -> Union[int, str]:
    """
    Calculate the balance number from the initials of the full name.
    Returns an int balance number or an error string.
    """
    from numerology_engine import reduce_number, PYTHAGOREAN_MAP

    if not full_name or not full_name.strip():
        return "Name Required"

    initials_sum = 0
    name_parts = full_name.upper().split()
    for part in name_parts:
        if part and part[0] in PYTHAGOREAN_MAP:
            initials_sum += PYTHAGOREAN_MAP[part[0]]

    if initials_sum == 0:
        return "Could not derive initials"

    return reduce_number(initials_sum)


def get_balance_analysis(balance_num: int) -> dict:
    """
    Given a balance number, return the detailed meaning dictionary.
    If invalid number, returns default 'error' structure.
    """
    meanings = _load_meanings()
    meaning = meanings.get(str(balance_num))

    if not meaning:
        return {
            "summary": "Invalid Balance Number. Please enter a valid number.",
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

    return meaning


def get_balance_report_string(balance_num: int) -> str:
    """
    Format a readable multi-line string report for the given balance number.
    """
    analysis = get_balance_analysis(balance_num)

    lines = [
        "=" * 60,
        f"⚖️ Balance {balance_num} Report ⚖️",
        "=" * 60,
        f"🧾 Summary: {analysis.get('summary', analysis.get('description', 'No description'))}"
    ]

    advice = analysis.get('advice')
    if advice:
        lines.append(f"💡 Advice: {advice}")

    lines.append(f"✨ Master Number: {'Yes' if analysis.get('master') else 'No'}")
    lines.append(f"🜂 Element: {analysis.get('element')}")
    lines.append(f"🎨 Color: {analysis.get('color')}")
    lines.append(f"🔮 Vibration: {analysis.get('vibration')}\n")

    if analysis.get('traits'):
        lines.append("🔑 Core Traits: " + ', '.join(analysis['traits']))
    if analysis.get('strengths'):
        lines.append("✅ Strengths: " + ', '.join(analysis['strengths']))
    if analysis.get('weaknesses'):
        lines.append("⚠️ Weaknesses: " + ', '.join(analysis['weaknesses']))

    if analysis.get('business'):
        lines.append("\n💼 Business Outlook:")
        lines.append(f" - {analysis['business']}")

    if analysis.get('relationships'):
        lines.append("\n❤️ Relationships:")
        lines.append(f" - {analysis['relationships']}")

    if analysis.get('purpose'):
        lines.append("\n🎯 Life Purpose:")
        lines.append(f" - {analysis['purpose']}")

    lines.append("=" * 60)
    return "\n".join(lines)
