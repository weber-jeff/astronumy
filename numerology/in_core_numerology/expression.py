import os
from ..numerology_engine import get_sum_of_all_letters, reduce_number
from ..report_builder import build_report_string
from ..static.utils import get_data_dir, load_json_file, safe_get

# Load expression meanings using centralized utils
data_dir = get_data_dir()
expression_meanings_path = os.path.join(data_dir, "expression_meanings.json")
expression_meanings = load_json_file(expression_meanings_path)

def calculate_expression(full_name: str) -> int:
    """Calculate Expression number using core functions."""
    name_for_calc = "".join(filter(str.isalpha, full_name))
    if not name_for_calc:
        raise ValueError("Name is required")
    
    expression_sum_raw = get_sum_of_all_letters(name_for_calc)
    return reduce_number(expression_sum_raw, keep_master=True)

def get_expression_analysis(number: int) -> dict:
    """Get expression meaning dictionary from JSON, with safe defaults."""
    meaning = expression_meanings.get(str(number), {})
    
    default = {
        "summary": "Invalid Expression Number. Please enter a valid number.",
        "advice": None,
        "master": False,
        "traits": [],
        "strengths": [],
        "weaknesses": [],
        "business": None,
        "relationships": None,
        "purpose": None,
        "color": None,
        "vibrations": None,
        "element": None,
    }

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
        "element": meaning.get("element", default["element"]),
    }

def get_expression_report(number: int) -> str:
    """Generate formatted expression report string."""
    analysis = get_expression_analysis(number)
    return build_report_string(number, "Expression", "🎭", analysis, include_element=True, include_color_vibrations=True)
