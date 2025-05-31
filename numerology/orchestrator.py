import traceback
from numerology.in_core_numerology.hidden_passion import (
    calculate_hidden_passion_number,
    get_hidden_passion_report_string,
    get_hidden_passion_analysis,
)
from numerology.in_core_numerology.life_path_report import (
    calculate_life_path_number,
    get_life_path_report_string,
    get_life_path_analysis,
)
from numerology.in_core_numerology.expression import (
    calculate_expression,
    get_expression_analysis,
    get_expression_report_string,
)
from numerology.in_core_numerology.soul_urge import (
    calculate_soul_urge_number,
    get_soul_urge_report_string,
    get_soul_urge_analysis,
)
from numerology.in_core_numerology.pinnacle import (
    calculate_pinnacle_numbers,
    get_pinnacle_report_string,
    get_pinnacle_analysis,
)
from numerology.in_core_numerology.personality import (
    calculate_personality_number,
    get_personality_report_string,
    get_personality_analysis,
)
from numerology.in_core_numerology.maturity import (
    calculate_maturity_number,
    get_maturity_report_string,
    get_maturity_analysis,
)
from numerology.in_core_numerology.karmic import (
    calculate_karmic_lesson_numbers,
    get_karmic_report_string,
    get_karmic_analysis,
)
from numerology.in_core_numerology.challenge import (
    calculate_challenge_numbers,
    get_challenge_report_string,
    get_challenge_analysis,
)
from numerology.in_core_numerology.birthday import (
    calculate_birthday_number,
    get_birthday_report_string,
    get_birthday_analysis,
)
from numerology.in_core_numerology.balance import (
    calculate_balance_number,
    get_balance_report_string,
    get_balance_analysis,
)


class NumerologyOrchestrator:
    def __init__(self, full_name: str, birth_date: str):
        self.full_name = full_name
        self.birth_date = birth_date

    def generate_full_report(self) -> str:
        sections = []

        # Hidden Passion
        try:
            hp_num = calculate_hidden_passion_number(self.full_name)
            sections.append(get_hidden_passion_report_string(hp_num))
        except Exception:
            sections.append("Error generating Hidden Passion report:\n" + traceback.format_exc())

        # Life Path
        try:
            lp_num = calculate_life_path_number(self.birth_date)
            sections.append(get_life_path_report_string(lp_num))
        except Exception:
            sections.append("Error generating Life Path report:\n" + traceback.format_exc())

        # Expression
        try:
            ex_num = calculate_expression(self.full_name)
            sections.append(get_expression_report_string(ex_num))
        except Exception:
            sections.append("Error generating Expression report:\n" + traceback.format_exc())

        # Soul Urge
        try:
            su_num = calculate_soul_urge_number(self.full_name)
            sections.append(get_soul_urge_report_string(su_num))
        except Exception:
            sections.append("Error generating Soul Urge report:\n" + traceback.format_exc())

        # Pinnacle (can be multiple numbers, handled accordingly)
        try:
            pinnacle_nums = calculate_pinnacle_numbers(self.birth_date)
            sections.append(get_pinnacle_report_string(pinnacle_nums))
        except Exception:
            sections.append("Error generating Pinnacle report:\n" + traceback.format_exc())

        # Personality
        try:
            pers_num = calculate_personality_number(self.full_name)
            sections.append(get_personality_report_string(pers_num))
        except Exception:
            sections.append("Error generating Personality report:\n" + traceback.format_exc())

        # Maturity
        try:
            mat_num = calculate_maturity_number(self.full_name, self.birth_date)
            sections.append(get_maturity_report_string(mat_num))
        except Exception:
            sections.append("Error generating Maturity report:\n" + traceback.format_exc())

        # Karmic Lessons
        try:
            karmic_nums = calculate_karmic_lesson_numbers(self.full_name)
            sections.append(get_karmic_report_string(karmic_nums))
        except Exception:
            sections.append("Error generating Karmic Lesson report:\n" + traceback.format_exc())

        # Challenge
        try:
            challenge_nums = calculate_challenge_numbers(self.birth_date)
            sections.append(get_challenge_report_string(challenge_nums))
        except Exception:
            sections.append("Error generating Challenge report:\n" + traceback.format_exc())

        # Birthday
        try:
            bday_num = calculate_birthday_number(self.birth_date)
            sections.append(get_birthday_report_string(bday_num))
        except Exception:
            sections.append("Error generating Birthday report:\n" + traceback.format_exc())

        # Balance
        try:
            balance_num = calculate_balance_number(self.full_name)
            sections.append(get_balance_report_string(balance_num))
        except Exception:
            sections.append("Error generating Balance report:\n" + traceback.format_exc())

        return "\n\n".join(sections)

    def generate_full_report_json(self) -> dict:
        json_report = {}

        # Hidden Passion
        try:
            hp_num = calculate_hidden_passion_number(self.full_name)
            json_report["hidden_passion"] = get_hidden_passion_analysis(hp_num)
        except Exception:
            json_report["hidden_passion"] = {"error": traceback.format_exc()}

        # Life Path
        try:
            lp_num = calculate_life_path_number(self.birth_date)
            json_report["life_path"] = get_life_path_analysis(lp_num)
        except Exception:
            json_report["life_path"] = {"error": traceback.format_exc()}

        # Expression
        try:
            ex_num = calculate_expression(self.full_name)
            json_report["expression"] = get_expression_analysis(ex_num)
        except Exception:
            json_report["expression"] = {"error": traceback.format_exc()}

        # Soul Urge
        try:
            su_num = calculate_soul_urge_number(self.full_name)
            json_report["soul_urge"] = get_soul_urge_analysis(su_num)
        except Exception:
            json_report["soul_urge"] = {"error": traceback.format_exc()}

        # Pinnacle
        try:
            pinnacle_nums = calculate_pinnacle_numbers(self.birth_date)
            json_report["pinnacle"] = get_pinnacle_analysis(pinnacle_nums)
        except Exception:
            json_report["pinnacle"] = {"error": traceback.format_exc()}

        # Personality
        try:
            pers_num = calculate_personality_number(self.full_name)
            json_report["personality"] = get_personality_analysis(pers_num)
        except Exception:
            json_report["personality"] = {"error": traceback.format_exc()}

        # Maturity
        try:
            mat_num = calculate_maturity_number(self.full_name, self.birth_date)
            json_report["maturity"] = get_maturity_analysis(mat_num)
        except Exception:
            json_report["maturity"] = {"error": traceback.format_exc()}

        # Karmic
        try:
            karmic_nums = calculate_karmic_lesson_numbers(self.full_name)
            json_report["karmic"] = get_karmic_analysis(karmic_nums)
        except Exception:
            json_report["karmic"] = {"error": traceback.format_exc()}

        # Challenge
        try:
            challenge_nums = calculate_challenge_numbers(self.birth_date)
            json_report["challenge"] = get_challenge_analysis(challenge_nums)
        except Exception:
            json_report["challenge"] = {"error": traceback.format_exc()}

        # Birthday
        try:
            bday_num = calculate_birthday_number(self.birth_date)
            json_report["birthday"] = get_birthday_analysis(bday_num)
        except Exception:
            json_report["birthday"] = {"error": traceback.format_exc()}

        # Balance
        try:
            balance_num = calculate_balance_number(self.full_name)
            json_report["balance"] = get_balance_analysis(balance_num)
        except Exception:
            json_report["balance"] = {"error": traceback.format_exc()}

        return json_report


if __name__ == "__main__":
    # Example usage - replace with real user data
    orchestrator = NumerologyOrchestrator(
        full_name="Jeffery Allen Louis Weber",
        birth_date="1987-05-08",
    )
    print("=== Full Text Report ===")
    print(orchestrator.generate_full_report())

    print("\n=== Full JSON Report ===")
    import json
    print(json.dumps(orchestrator.generate_full_report_json(), indent=4, ensure_ascii=False))
