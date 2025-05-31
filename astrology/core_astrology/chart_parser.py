import os
import datetime
import logging
from typing import Dict, List, Union

import swisseph as swe

logging.basicConfig(level=logging.WARNING)  # Library-level default logging
logger = logging.getLogger(__name__)

try:
    
    from core_astrology.planetary_positions import get_planet_positions
  
except ImportError as e:
    logger.warning(f"Import fallback in chart_parser.py: {e}")

    def get_moon_sign(year: int, month: int, day: int,
                      hour: int, minute: int,
                      lat: float, lon: float, alt: float = 0) -> str:
        return "Error: get_moon_sign not loaded"

    def degree_to_sign(degree: float) -> str:
        return "Error: degree_to_sign not loaded"

    def get_planet_positions(year: int, month: int, day: int,
                              hour: int, minute: int,
                              lat: float, lon: float, alt: float = 0) -> dict:
        return {"error": "get_planet_positions not loaded"}

    def calculate_aspects(planet_positions: dict) -> dict:
        return {"error": "calculate_aspects not loaded"}

    def assign_planets_to_houses(planet_positions: dict,
                                 house_cusps: List[float]) -> dict:
        return {"error": "assign_planets_to_houses not loaded"}


def _to_utc_datetime(year: int, month: int, day: int,
                     hour: int, minute: int,
                     ut_offset: float) -> datetime.datetime:
    """
    Convert local time with UTC offset to an aware UTC datetime.

    Args:
        year, month, day, hour, minute: Local time components
        ut_offset: Timezone offset from UTC in hours (e.g. -5 for EST)

    Returns:
        datetime.datetime object with UTC timezone
    """
    local_dt = datetime.datetime(year, month, day, hour, minute)
    utc_dt = local_dt - datetime.timedelta(hours=ut_offset)
    return utc_dt.replace(tzinfo=datetime.timezone.utc)


def _validate_inputs(year: int, month: int, day: int,
                     hour: int, minute: int,
                     lat: float, lon: float) -> None:
    if not (1 <= month <= 12):
        raise ValueError("Month must be between 1 and 12")
    if not (1 <= day <= 31):
        raise ValueError("Day must be between 1 and 31")
    if not (0 <= hour < 24):
        raise ValueError("Hour must be between 0 and 23")
    if not (0 <= minute < 60):
        raise ValueError("Minute must be between 0 and 59")
    if not (-90 <= lat <= 90):
        raise ValueError("Latitude must be between -90 and 90")
    if not (-180 <= lon <= 180):
        raise ValueError("Longitude must be between -180 and 180")


def _check_for_error(result: dict, context: str) -> bool:
    """
    Helper to check dict for 'error' key, log it, and return True if error found.
    """
    if "error" in result:
        logger.error(f"{context} error: {result['error']}")
        return True
    return False


def generate_birth_chart(
    year: int,
    month: int,
    day: int,
    hour: int = 12,
    minute: int = 0,
    ut_offset: float = 0.0,
    lat: float = 0.0,
    lon: float = 0.0,
    alt: float = 0.0,
    house_system: str = 'P'
) -> Dict[str, Union[str, float, dict, List[float]]]:
    """
    Generate a complete birth chart dictionary using Swiss Ephemeris.

    Parameters:
        year, month, day, hour, minute: Local birth date/time components
        ut_offset: Timezone offset hours to UTC (e.g. -5.0 for EST)
        lat, lon, alt: Geographic coordinates (degrees, meters)
        house_system: House calculation system (default 'P' = Placidus)

    Returns:
        dict: Birth chart data or {'error': str} on failure
    """
    try:
        _validate_inputs(year, month, day, hour, minute, lat, lon)
        ut_dt = _to_utc_datetime(year, month, day, hour, minute, ut_offset)

        # More precise fractional hour including microseconds
        frac_hour = (
            ut_dt.hour
            + ut_dt.minute / 60.0
            + ut_dt.second / 3600.0
            + ut_dt.microsecond / 3_600_000_000.0
        )
        jd_ut = swe.julday(ut_dt.year, ut_dt.month, ut_dt.day, frac_hour)

        swe.set_topo(lon, lat, alt)

        planet_positions = get_planet_positions(
            ut_dt.year, ut_dt.month, ut_dt.day,
            ut_dt.hour, ut_dt.minute, lat, lon, alt
        )
        if _check_for_error(planet_positions, "Planet positions"):
            return {"error": planet_positions["error"]}

        moon_sign = get_moon_sign(
            ut_dt.year, ut_dt.month, ut_dt.day,
            ut_dt.hour, ut_dt.minute, lat, lon, alt
        )
        if moon_sign.startswith("Error"):
            logger.error(f"Moon sign error: {moon_sign}")
            return {"error": moon_sign}

        aspects = calculate_aspects(planet_positions)
        if _check_for_error(aspects, "Aspects"):
            return {"error": aspects["error"]}

        house_cusps, ascmc = swe.houses(jd_ut, lat, lon, house_system.encode())
        planet_houses = assign_planets_to_houses(planet_positions, list(house_cusps))
        if _check_for_error(planet_houses, "House assignment"):
            return {"error": planet_houses["error"]}

        return {
            "birth_datetime_utc": ut_dt.strftime("%Y-%m-%d %H:%M:%S UT"),
            "julian_day_ut": jd_ut,
            "geo_location": {"latitude": lat, "longitude": lon, "altitude": alt},
            "planet_positions": planet_positions,
            "moon_sign": moon_sign,
            "aspects": aspects,
            "house_cusps_placidus": list(house_cusps),
            "ascendant_longitude": ascmc[0],
            "mc_longitude": ascmc[1],
            "vertex_longitude": ascmc[3],
            "planet_houses": planet_houses,
            "house_system": house_system
        }

    except Exception as e:
        logger.error("Unexpected error in generate_birth_chart", exc_info=True)
        return {"error": f"Unexpected error: {str(e)}"}


if __name__ == "__main__":
    print("=== Birth Chart Generator Test ===")
    ephe_path = os.environ.get('SWEP_PATH', '/media/jeff/numy/numerology_ai/mp/')
    if os.path.isdir(ephe_path):
        swe.set_ephe_path(ephe_path)
        print(f"Ephemeris path set: {ephe_path}")
    else:
        print(f"WARNING: Ephemeris not found at '{ephe_path}'")

    test_data = {
        "year": 1990, "month": 3, "day": 15,
        "hour": 14, "minute": 30, "ut_offset": -5.0,
        "lat": 40.7128, "lon": -74.0060, "alt": 0.0,
        "house_system": 'P'
    }
    print(f"\nGenerating for: {test_data}")
    result = generate_birth_chart(**test_data)
    if "error" in result:
        print("ERROR:", result["error"])
    else:
        print("Moon Sign:", result["moon_sign"])
        print("Ascendant:", f"{result['ascendant_longitude']:.2f}")
        print("MC:", f"{result['mc_longitude']:.2f}")
