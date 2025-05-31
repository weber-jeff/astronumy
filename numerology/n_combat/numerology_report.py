import sys
import os

# Add project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import calculation utilities
from numerology.numerology_engine import (
    calclate_life_path,
    calculate_expression_number,
    calculate_soul_urge_number,
    calculate_personality_number,
    calculate_birthday_number, # Though birthday day is often passed directly
    calculate_balance_number, # If you calculate it from name initials
    calculate_maturity_number,
    calculate_hidden_passion_number,
    calculate_karmic_lesson_number
)
from numerology.in_core_numerology.karmic import get_karmic_lesson_analysis

from numerology.in_core_numerology.birthday import get_birthday_report_string
from numerology.meanings.balance import get_balance_report_string
from numerology.in_core_numerology.expression import get_expression_analysis, get_expression_report_string
from numerology.meanings.challenge import get_challenge_analysis, get_challenge_report_string # Corrected module name

def generate_full_numerology_report(user_data: dict) -> str:
    report_sections = []

    # 🔢 Birthday Report
    if 'birthday' in user_data:
        try:
            birthday_day = int(user_data['birthday'])
            if 1 <= birthday_day <= 31:
                report_sections.append(get_birthday_report_string(birthday_day))
            else:
                report_sections.append("❗ Invalid birthday day. Must be between 1 and 31.")
        except (ValueError, TypeError):
            report_sections.append("❗ Invalid birthday format. Expected day as integer (1–31).")

    # ⚖️ Balance Number Report
    # Assuming balance number is passed directly. If calculated from name, adjust accordingly.
    if 'balance_number' in user_data: # Changed key for clarity
        try:
            balance_num = int(user_data['balance_number'])
            report_sections.append(get_balance_report_string(balance_num))
        except (ValueError, TypeError):
            report_sections.append("❗ Invalid Balance Number format. Expected integer.")

    # 🎭 Expression Report
    if 'full_name' in user_data and user_data['full_name']:
        try:
            full_name = user_data['full_name']
            expression_number_val = calculate_expression_number(full_name)
            if isinstance(expression_number_val, int):
                analysis = get_expression_analysis(expression_number_val)
                report_sections.append(get_expression_report_string(analysis))
            else:
                # expression_number_val might be an error string from the calculation
                report_sections.append(f"❗ Could not calculate Expression Number: {expression_number_val}")
        except Exception as e:
            report_sections.append(f"❗ Error generating Expression Report: {e}")
    elif 'full_name' in user_data and not user_data['full_name']:
        report_sections.append("❗ Full name not provided for Expression Report.")

# 🎭 Expression Report
if 'full_name' in user_data and user_data['full_name']:
    try:
        full_name = user_data['full_name']
        expression_number_val = calculate_expression_number(full_name)
        if isinstance(expression_number_val, int):
            analysis = get_expression_analysis(expression_number_val)
            report_sections.append(get_expression_report_string(analysis))
        else:
            report_sections.append(f"❗ Could not calculate Expression Number: {expression_number_val}")
    except Exception as e:
        report_sections.append(f"❗ Error generating Expression Report: {e}")
elif 'full_name' in user_data and not user_data['full_name']:
    report_sections.append("❗ Full name not provided for Expression Report.")

# Inside your main report generation code, e.g., after you have user_data and report_sections list:

    if 'karmic_lessons' in user_data and user_data['karmic_lessons']:
        try:
            karmic_lessons = user_data['karmic_lessons']
            # Expecting a list of integers, e.g., [1, 2]
            if isinstance(karmic_lessons, list) and all(isinstance(x, int) for x in karmic_lessons):
                karmic_analysis = get_karmic_lesson_analysis(karmic_lessons)
                report_sections.append(karmic_analysis)
            else:
                report_sections.append("❗ Karmic lessons data is invalid or not a list of integers.")
        except Exception as e:
            report_sections.append(f"❗ Error generating Karmic Lessons Report: {e}")
    elif 'karmic_lessons' in user_data and not user_data['karmic_lessons']:
        report_sections.append("❗ Karmic lessons data is empty or missing.")

from numerology.numerology_engine import calculate_challenge_numbers
from numerology.meanings.challenge import get_challenge_report_string

def generate_full_numerology_report(user_data):
    report_sections = []

    if 'birth_date' in user_data and user_data['birth_date']:
        try:
            birth_date_str = user_data['birth_date']
            challenge_numbers_list = challenge_numbers_list = calculate_challenge_numbers(birth_date_str)


            if isinstance(challenge_numbers_list, str):
                report_sections.append(f"❗ Could not calculate Challenge Numbers: {challenge_numbers_list}")
            elif challenge_numbers_list and all(isinstance(cn, int) for cn in challenge_numbers_list):
                report_sections.append("============================================================")
                report_sections.append("🏔️ Challenge Numbers Overview 🏔️")
                report_sections.append("============================================================")
                for idx, num in enumerate(challenge_numbers_list):
                    report_sections.append(f"\n🔹 Challenge {idx + 1}:")
                    report_sections.append(get_challenge_report_string(num))
            else:
                report_sections.append(f"❗ Issues calculating some Challenge Numbers: {challenge_numbers_list}")

        except Exception as e:
            report_sections.append(f"❗ Error generating Challenge Numbers Report: {e}")
    else:
        report_sections.append("❗ No valid birth_date provided for Challenge Number calculation.")

    # 🧩 Add other reports here, e.g., Life Path, Expression...

    return "\n\n".join(report_sections)  # Double newline between sections


if __name__ == "__main__":
    user_data = {
        "full_name": "Jane Doe",
        "birthday": "8",
        "balance_number": 4,
        "birth_date": "1990-05-08",
    }

    full_report = generate_full_numerology_report(user_data)
    print(full_report)
def generate_full_report(name: str, dob: str) -> str:
    from datetime import datetime

    # Split and validate DOB
    birth_date = datetime.strptime(dob, "%Y-%m-%d")
    day = birth_date.day
    month = birth_date.month
    year = birth_date.year

    # Calculate all necessary numbers
    life_path = reduce_to_life_path_number(dob)
    expression = reduce_to_expression_number(name)
    soul_urge = reduce_to_soul_urge_number(name)
    personality = reduce_to_personality_number(name)
    birthday = day
    karmic = get_karmic_lessons(name)
    hidden_passion = get_hidden_passion_analysis(name)
    balance = reduce_to_balance_number(expression)  # or other logic
    pinnacle = get_pinnacle_analysis(dob)
    challenge = get_challenge_analysis(dob)
    personal_year = get_personal_year_number(dob)
    personal_month = get_personal_month_number(dob)
    personal_day = get_personal_day_number(dob)

    # Start assembling report
    report = "="*60 + f"\n🔢 Full Numerology Report for: {name} (DOB: {dob})\n" + "="*60 + "\n"

    # Life Path
    life_path_data = get_life_path_analysis(dob)
    report += f"\n🔮 Life Path Number: {life_path}\nMeaning: {life_path_data['summary']}\n"

    # Expression
    expr_data = get_expression_analysis(name)
    report += f"\n🗣️ Expression Number: {expression}\nMeaning: {expr_data['summary']}\n"

    # Soul Urge
    soul_data = get_soul_urge_analysis(name)
    report += f"\n💓 Soul Urge Number: {soul_urge}\nMeaning: {soul_data['summary']}\n"

    # Personality
    pers_data = get_personality_analysis(name)
    report += f"\n🎭 Personality Number: {personality}\nMeaning: {pers_data['summary']}\n"

    # Birthday
    bday_data = get_birthday_analysis(day)
    report += f"\n🎂 Birthday Number: {birthday}\nMeaning: {bday_data['summary']}\n"

    # Karmic Lessons
    if karmic['lessons']:
        report += f"\n🔗 Karmic Lessons:\nMissing Numbers: {', '.join(map(str, karmic['lessons']))}\n"
        for num, lesson in karmic['meanings'].items():
            report += f"Lesson {num}: {lesson}\n"
    else:
        report += "\n🔗 Karmic Lessons: None – all numbers present.\n"

    # Hidden Passion
    report += f"\n🔥 Hidden Passion Number: {hidden_passion['number']}\nDescription: {hidden_passion['description']}\n"

    # Balance
    balance_data = get_balance_analysis(expression)
    report += (
        f"\n⚖️ Balance Number: {balance}\n"
        f"{balance_data['summary']}\nAdvice: {balance_data['advice']}\n"
    )

    # Pinnacles
    report += f"\n🌄 Pinnacle Numbers:\n"
    for i, pin in enumerate(pinnacle['pinnacles'], 1):
        report += f"{i}st Pinnacle: {pin['number']} – {pin['meaning']}\n"

    # Challenges
    report += f"\n🧗 Challenge Numbers:\n"
    for i, ch in enumerate(challenge['challenges'], 1):
        report += f"{i}st Challenge: {ch['number']} – {ch['meaning']}\n"

    # Personal Year/Month/Day
    report += (
        f"\n📆 Personal Year: {personal_year}\n"
        f"{get_personal_year_analysis(personal_year)}\n"
        f"📅 Personal Month: {personal_month}\n"
        f"{get_personal_month_analysis(personal_month)}\n"
        f"📅 Personal Day: {personal_day}\n"
        f"{get_personal_day_analysis(personal_day)}\n"
    )

    # Optional: Color & Vibration (can come from Life Path or Expression, or own system)
    report += f"\n🎨 Color: {life_path_data.get('color', 'N/A')}\n"
    report += f"🔊 Vibration: {life_path_data.get('vibration', 'N/A')}\n"

    # Footer
    report += "\n" + "="*60 + "\n📝 Final Thoughts:\nUse your numbers as a compass, not a cage. Grow with awareness.\n" + "="*60 + "\n"

    return report
print(generate_full_report("John Doe", "1990-06-25"))
