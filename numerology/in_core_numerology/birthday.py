from typing import Dict

# Import reduce_number from the numerology_engine.py file,
# which is located in the parent directory ('numerology').
from ..numerology_engine import reduce_number

def get_reduced_date_components(birth_date_str: str) -> Dict[str, int]:
    """
    Calculates the reduced day, month, and year from a birth date string.
    Expects birth_date_str in 'YYYY-MM-DD' format.

    Example:
    "1990-05-16" -> day: 7 (1+6), month: 5, year: 1 (1+9+9+0=19 -> 1+0=1)
    """
    try:
        year_s, month_s, day_s = birth_date_str.split('-')
    except ValueError:
        raise ValueError("Birth date must be in 'YYYY-MM-DD' format for get_reduced_date_components.")

    # Day Number: Reduce the day of the month.
    reduced_day = reduce_number(int(day_s))

    # Month Number: Reduce the month number.
    reduced_month = reduce_number(int(month_s))

    # Year Number: Sum all digits of the year and reduce that sum.
    year_sum_digits = sum(int(digit) for digit in year_s)
    reduced_year = reduce_number(year_sum_digits)

    return {
        "day": reduced_day,
        "month": reduced_month,
        "year": reduced_year,
    }