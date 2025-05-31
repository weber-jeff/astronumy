import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
import swisseph as swe

# === Constants ===
PLANET_LIST = {
    "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY, "Venus": swe.VENUS,
    "Mars": swe.MARS, "Jupiter": swe.JUPITER, "Saturn": swe.SATURN, "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE, "Pluto": swe.PLUTO, "Chiron": swe.CHIRON, "TrueNode": swe.TRUE_NODE,
}

ZODIAC_GLYPHS = {
    "Aries": "♈", "Taurus": "♉", "Gemini": "♊", "Cancer": "♋", "Leo": "♌", "Virgo": "♍",
    "Libra": "♎", "Scorpio": "♏", "Sagittarius": "♐", "Capricorn": "♑", "Aquarius": "♒", "Pisces": "♓",
}

# === File Loader ===
def load_json_file(filename: str) -> Dict[str, Any]:
    path = os.path.join(os.path.dirname(__file__), 'meanings', filename)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Could not load {filename}: {e}")
        return {}

# === Helper Functions ===
def degree_to_sign(degree: float) -> str:
    signs = list(ZODIAC_GLYPHS.keys())
    return signs[int(degree // 30) % 12]

def format_longitude(degree: float) -> str:
    sign = degree_to_sign(degree)
    glyph = ZODIAC_GLYPHS[sign]
    deg_in_sign = degree % 30
    deg = int(deg_in_sign)
    min_float = (deg_in_sign - deg) * 60
    minute = int(min_float)
    second = int((min_float - minute) * 60)
    return f"{deg:02d}°{glyph} {sign} {minute:02d}'{second:02d}\""

# === Astrology Calculators ===
def calculate_julian_day(year: int, month: int, day: int, hour: float, ut_offset: float) -> float:
    return swe.julday(year, month, day, hour) - (ut_offset / 24.0)

def get_planet_positions(jd_ut: float) -> Dict[str, Optional[float]]:
    positions = {}
    for name, pid in PLANET_LIST.items():
        try:
            lon = swe.calc_ut(jd_ut, pid)[0][0]
            positions[name] = lon
        except swe.SwissephError:
            positions[name] = None
    return positions

def get_ascendant(jd_ut: float, lat: float, lon: float) -> Optional[float]:
    try:
        _, ascmc = swe.houses(jd_ut, lat, lon)
        return ascmc[0]
    except swe.SwissephError:
        return None

# === Report Builders ===
def generate_planet_section(positions: Dict[str, Optional[float]], meanings: Dict[str, Any]) -> str:
    lines = ["🌌 Planetary Placements:"]
    for name, lon in positions.items():
        if lon is None:
            lines.append(f"  {name}: Position unavailable")
            continue
        sign = degree_to_sign(lon)
        meaning = meanings.get(name, {}).get("summary", "No meaning available.")
        lines.append(f"  {name}: {format_longitude(lon)} in {sign}")
        lines.append(f"    ✦ Meaning: {meaning}")
    return "\n".join(lines) + "\n"

def generate_ascendant_section(asc: Optional[float], meanings: Dict[str, Any]) -> str:
    if asc is None:
        return "↑ Ascendant: Position unavailable\n"
    sign = degree_to_sign(asc)
    meaning = meanings.get(sign, {}).get("summary", "No Ascendant meaning available.")
    return f"↑ Ascendant: {format_longitude(asc)} ({sign})\n   Meaning: {meaning}\n"

# === High-Level Report ===
def generate_astrology_report(
    year: int, month: int, day: int,
    hour: int, minute: int,
    lon: float, lat: float,
    ut_offset: float = 0.0,
    eph_path: Optional[str] = None
) -> str:

    # Set Swiss Ephemeris path
    swe.set_ephe_path(eph_path or "/usr/share/ephe")

    jd_ut = calculate_julian_day(year, month, day, hour + minute / 60.0, ut_offset)

    # Load interpretations
    planet_meanings = load_json_file("planet_meanings.json")
    ascendant_meanings = load_json_file("rising_sign_meanings.json")

    # Compute planetary positions and ascendant
    planets = get_planet_positions(jd_ut)
    ascendant = get_ascendant(jd_ut, lat, lon)

    # Format report
    birth_str = datetime(year, month, day, hour, minute).strftime("%B %d, %Y, %I:%M %p")

    report = [
        "===== Natal Astrology Report =====",
        f"Birth Date (Local): {birth_str}",
        f"Birth Location: Lat {lat:.2f}, Lon {lon:.2f}",
        "----------------------------------\n",
        generate_ascendant_section(ascendant, ascendant_meanings),
        generate_planet_section(planets, planet_meanings),
        "--- End of Report ---"
    ]
    return "\n".join(report)

# === CLI Entry Point ===
if __name__ == "__main__":
    eph_path = os.environ.get("SWEP_PATH", "/usr/share/ephe")
    if not os.path.isdir(eph_path):
        print(f"[ERROR] Ephemeris path '{eph_path}' not found.")
    else:
        sample_report = generate_astrology_report(
            year=1990, month=3, day=15,
            hour=14, minute=30,
            lon=-74.0060, lat=40.7128,
            ut_offset=-5.0,
            eph_path=eph_path
        )
        print(sample_report)
