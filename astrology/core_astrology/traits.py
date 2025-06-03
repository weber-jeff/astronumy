
import swisseph as swe
import datetime
import os
from typing import Optional, Dict, Any
import datetime # Added for type hint in generate_birth_chart fallback if needed
import json # For safe_load_meaning

def safe_load_meaning(filename: str) -> dict:
    try:
        # Assuming load_meaning is in astrology.astro_data.load_meanings
        # Adjust path if it's different or if load_meanings.py is in the same directory
        from astrology.astro_data.json.load_meanings import load_meaning
        return load_meaning(filename)
    except ImportError as e:
        print(f"Warning: Could not import 'load_meaning' function: {e}")
        return {}
    except Exception as e: # Catch other errors during loading (e.g., file not found by load_meaning)
        print(f"Warning: Failed to load meanings from {filename}: {e}")
        return {}

# === Imports for astrology data and utilities ===
# Load all meanings with one-liner calls
aspect_meanings = safe_load_meaning("aspect_meanings.json")
planet_meanings = safe_load_meaning("planet_meanings.json")
house_meanings = safe_load_meaning("house_meanings.json")
rising_sign_meanings = safe_load_meaning("rising_sign_meanings.json")
moon_sign_meanings = safe_load_meaning("moon_sign_meanings.json")
sign_meanings = safe_load_meaning("sign_meanings.json")
element_meanings = safe_load_meaning("element_meanings.json")
modality_meanings = safe_load_meaning("modality_meanings.json")
p_aspects = safe_load_meaning("p_aspects.json") 
planet_in_house_meanings = safe_load_meaning("planet_in_house_meanings.json")
rising_sign_meanings = safe_load_meaning("rising_sign_meanings.json")
sign_meanings = safe_load_meaning("sign_meanings.json")

try:
    from astrology.astro_data.json.load_meanings import load_meaning
    from astrology.astro_data.glyphs import aspect_glyphs

except ImportError as e:
    print(f"Warning: Could not import some astro_data files: {e}")
    aspect_meanings = {}
    planet_meanings = {}
    house_meanings = {}
    rising_sign_meanings = {}
    moon_sign_meanings = {}
    sign_meanings = {}
    element_meanings = {}
    modality_meanings = {}
    p_aspects = {}
    planet_in_house_meanings = {}

    def get_aspect_report(aspect_name: str) -> str:
        return f"Aspect report unavailable for {aspect_name}"


       


try:
    from astrology.core_astrology.chart_parser import (
        get_sun_sign,
        get_moon_sign,
        get_sign_details,
        degree_to_sign,
        element,
        modality,
        calculate_aspects_within_chart,
        PLANET_NAMES,
        ASPECT_ANGLES,
        ASPECT_TYPES,
    )
except ImportError as e:
    print(f"Warning: Could not import zodiac utilities: {e}")

    # Fallback stubs for zodiac functions
    def get_sun_sign(m, d): return "Unknown"
    def get_moon_sign(y, m, d, h, mi, lat, lon, alt=0): return "Unknown"
    def degree_to_sign(lon): return "Unknown"
    element = lambda x: "Unknown"
    modality = lambda x: "Unknown"
    calculate_aspects_within_chart = lambda x, y: []
    PLANET_NAMES, ASPECT_ANGLES, ASPECT_TYPES = {}, {}, {}


try:
    from astrology.core_astrology.chart_parser import generate_birth_chart, get_planet_positions
except ImportError as e:
    print(f"Warning: Could not import chart parsing utilities: {e}")

    def generate_birth_chart(*args, **kwargs):
        return {"error": "Birth chart generation unavailable"}

    def get_planet_positions(*args, **kwargs):
        return {"error": "Planet positions unavailable"}

try:
    from astrology.astro_data.json.load_meanings import get_aspect_report, rising_sign_meanings, get_house_report_string
except ImportError as e:
    print(f"Warning: Could not import rising sign meanings: {e}")

    def get_house_report_string(house_number: int) -> str:
        return f"House {house_number} report unavailable"

# === Helper function ===

def format_longitude(lon: float) -> str:
    """
    Converts a longitude in degrees into a string formatted as:
    degrees° SignName minutes'seconds"
    """
    sign_name = degree_to_sign(lon)
    deg_in_sign = lon % 30
    degrees = int(deg_in_sign)
    minutes_full = (deg_in_sign - degrees) * 60
    minutes = int(minutes_full)
    seconds = int((minutes_full - minutes) * 60)
    return f"{degrees:02d}° {sign_name} {minutes:02d}'{seconds:02d}\""


# Use this local list to avoid import issues or inconsistencies
PLANET_LIST_FOR_REPORT = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
    "Chiron": swe.CHIRON,
    "TrueNode": swe.TRUE_NODE,
}

def generate_astrology_report(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    lon: float,
    lat: float,
    ut_offset: float = 0.0,
    alt: float = 0,
) -> str:
    """
    Generates a detailed natal astrology report based on birth data.
    """

    chart_data = generate_birth_chart(year, month, day, hour, minute, ut_offset, lat, lon, alt)

    if "error" in chart_data:
        return f"Error generating birth chart: {chart_data['error']}"

    report_lines = []
    report_lines.append("===== Natal Astrology Report =====")
    report_lines.append(f"Birth Date (Local): {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}")
    report_lines.append(f"Birth Location: Lat {lat:.2f}, Lon {lon:.2f}")

    if "birth_datetime_utc" in chart_data:
        report_lines.append(f"Birth Date (UTC): {chart_data['birth_datetime_utc']}")

    report_lines.append("----------------------------------\n")

    # Sun
    sun_longitude = chart_data.get("planet_positions", {}).get("Sun")
    if isinstance(sun_longitude, float):
        sun_sign = degree_to_sign(sun_longitude)
        report_lines.append(f"☉ Sun: {format_longitude(sun_longitude)} ({sun_sign})")
        sign_def = sign_meanings.get(sun_sign, {})
        report_lines.append(f"   Summary: {sign_def.get('summary', 'No summary available.')}\n")
    else:
        report_lines.append("☉ Sun: Position unavailable\n")

    # Moon
    moon_longitude = chart_data.get("planet_positions", {}).get("Moon")
    natal_moon_sign = chart_data.get("moon_sign", "N/A")
    if isinstance(moon_longitude, float):
        report_lines.append(f"☽ Moon: {format_longitude(moon_longitude)} ({natal_moon_sign})")
        # TODO: Replace placeholder with real moon sign interpretation if available
        report_lines.append(f"   Meaning: The Moon represents your emotional nature... In {natal_moon_sign}, this suggests... (interpretation pending)\n")
    else:
        report_lines.append(f"☽ Moon: Position unavailable or {natal_moon_sign}\n")

    # Ascendant (Rising sign)
    asc_longitude = chart_data.get("ascendant_longitude")
    if isinstance(asc_longitude, float):
        asc_sign = degree_to_sign(asc_longitude)
        report_lines.append(f"↑ Ascendant (Rising Sign): {format_longitude(asc_longitude)} ({asc_sign})")
        report_lines.append(f"   Meaning: Your Ascendant describes your outward personality and approach to life. In {asc_sign}, it suggests... (interpretation pending)\n")
    else:
        report_lines.append("↑ Ascendant: Calculation unavailable\n")

    # House Reports
    report_lines.append("\n--- House Reports ---")
    for house_number in range(1, 13):
        report_lines.append(get_house_report_string(house_number))

    # Planetary Placements
    report_lines.append("\nPlanetary Placements:")
    planet_positions = chart_data.get("planet_positions", {})
    planet_houses = chart_data.get("planet_houses", {})

    for planet_name in PLANET_LIST_FOR_REPORT.keys():
        lon_val = planet_positions.get(planet_name)
        house_num = planet_houses.get(planet_name, "N/A")
        if isinstance(lon_val, float):
            sign = degree_to_sign(lon_val)
            report_lines.append(f"  {planet_name} in {sign} (House {house_num}): {format_longitude(lon_val)}")
        else:
            report_lines.append(f"  {planet_name}: Position unavailable")

    # Key Aspects
    report_lines.append("\nKey Aspects:")
    aspects = chart_data.get("aspects", [])

    if isinstance(aspects, list) and aspects:
        # Handle placeholder info or real aspects
        if (isinstance(aspects[0], dict) and "info" in aspects[0] and "Placeholder" in aspects[0]["info"]):
            report_lines.append(f"  {aspects[0]['info']}")
        else:
            # Limit output to first 5 aspects for brevity
            for aspect_info in aspects[:5]:
                p1 = aspect_info.get("planet1")
                asp_type = aspect_info.get("aspect_type")
                p2 = aspect_info.get("planet2")
                orb = aspect_info.get("orb")
                if p1 and asp_type and p2:
                    report_lines.append(f"  - {p1} {asp_type} {p2} (Orb: {orb:.1f}°)")
                    # Add detailed aspect report (safe call)
                    report_lines.append(get_aspect_report(asp_type))
                else:
                    report_lines.append(f"  - Incomplete aspect data: {aspect_info}")
    elif isinstance(aspects, dict) and "info" in aspects:
        report_lines.append(f"  {aspects['info']}")
    else:
        report_lines.append("  No significant aspects or aspect data unavailable.")

    report_lines.append("\n--- End of Astrology Report ---")

    return "\n".join(report_lines)


if __name__ == "__main__":
    # Attempt to set Swiss Ephemeris path
    eph_path = os.environ.get('SWEP_PATH', '/media/jeff/numy/numerology_ai/mp/')
    if os.path.isdir(eph_path):
        try:
            swe.set_ephe_path(eph_path)
            print(f"Swiss Ephemeris path set to: {eph_path}")
            # Generate a sample report
            print("\n--- Generating Sample Astrology Report ---")
            sample_report = generate_astrology_report(
                1990, 3, 15, 14, 30, -74.0060, 40.7128, ut_offset=-5.0
            )
            print(sample_report)
        except Exception as e:
            print(f"Error during report generation: {e}")
    else:
        print(f"Warning: Swiss Ephemeris path does not exist: {eph_path}")
        print("Skipping astrology report generation.")
                glyph = aspect_glyphs.get(asp_type, asp_type)
                aspect_desc = get_aspect_report(asp_type)
                report_lines.append(
                    f"  {p1} {glyph} {p2} (Orb: {orb:.2f}°) - {aspect_desc}"
                )
    else:
        report_lines.append("  No significant aspects calculated or available.")

    report_lines.append("\n==================================")
    return "\n".join(report_lines)
you sope