import swisseph as swe
from datetime import datetime
from functools import lru_cache
from typing import Dict, Optional, Union
import pytz
import logging

# --- Setup Logger ---
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# --- Zodiac Sign Data ---
ZODIAC_SIGNS = [
    {"name": "Aries", "start": (3, 21), "end": (4, 19), "element": "Fire", "modality": "Cardinal", "symbol": "♈", "longitude_start": 0},
    {"name": "Taurus", "start": (4, 20), "end": (5, 20), "element": "Earth", "modality": "Fixed", "symbol": "♉", "longitude_start": 30},
    {"name": "Gemini", "start": (5, 21), "end": (6, 20), "element": "Air", "modality": "Mutable", "symbol": "♊", "longitude_start": 60},
    {"name": "Cancer", "start": (6, 21), "end": (7, 22), "element": "Water", "modality": "Cardinal", "symbol": "♋", "longitude_start": 90},
    {"name": "Leo", "start": (7, 23), "end": (8, 22), "element": "Fire", "modality": "Fixed", "symbol": "♌", "longitude_start": 120},
    {"name": "Virgo", "start": (8, 23), "end": (9, 22), "element": "Earth", "modality": "Mutable", "symbol": "♍", "longitude_start": 150},
    {"name": "Libra", "start": (9, 23), "end": (10, 22), "element": "Air", "modality": "Cardinal", "symbol": "♎", "longitude_start": 180},
    {"name": "Scorpio", "start": (10, 23), "end": (11, 21), "element": "Water", "modality": "Fixed", "symbol": "♏", "longitude_start": 210},
    {"name": "Sagittarius", "start": (11, 22), "end": (12, 21), "element": "Fire", "modality": "Mutable", "symbol": "♐", "longitude_start": 240},
    {"name": "Capricorn", "start": (12, 22), "end": (1, 19), "element": "Earth", "modality": "Cardinal", "symbol": "♑", "longitude_start": 270},
    {"name": "Aquarius", "start": (1, 20), "end": (2, 18), "element": "Air", "modality": "Fixed", "symbol": "♒", "longitude_start": 300},
    {"name": "Pisces", "start": (2, 19), "end": (3, 20), "element": "Water", "modality": "Mutable", "symbol": "♓", "longitude_start": 330},
]

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO
}

ASPECT_ANGLES = {
    0: "Conjunction",
    60: "Sextile",
    90: "Square",
    120: "Trine",
    180: "Opposition"
}
ASPECT_ORB = 6  # degrees tolerance

# --- Utility Functions ---

def normalize_angle(angle: float) -> float:
    """Normalize angle to [0, 360) degrees."""
    return angle % 360

def get_sun_sign(month: int, day: int) -> str:
    """Determine the Sun sign based on birth month/day."""
    for sign in ZODIAC_SIGNS:
        start_m, start_d = sign["start"]
        end_m, end_d = sign["end"]
        if start_m < end_m:
            if (month == start_m and day >= start_d) or (month == end_m and day <= end_d) or (start_m < month < end_m):
                return sign["name"]
        else:  # Capricorn wrap-around
            if (month == start_m and day >= start_d) or (month == end_m and day <= end_d) or (month > start_m or month < end_m):
                return sign["name"]
    return "Unknown"

def degree_to_sign(longitude: float) -> str:
    """Map ecliptic longitude to Zodiac sign."""
    longitude = normalize_angle(longitude)
    for sign in ZODIAC_SIGNS:
        start = sign["longitude_start"]
        end = (start + 30) % 360
        if start < end:
            if start <= longitude < end:
                return sign["name"]
        else:  # Pisces wrap-around
            if longitude >= start or longitude < end:
                return sign["name"]
    return "Unknown"

def calculate_aspect(angle_diff: float) -> Optional[str]:
    """Return aspect name if angle difference is within orb."""
    angle_diff = angle_diff % 360
    if angle_diff > 180:
        angle_diff = 360 - angle_diff
    for angle, name in ASPECT_ANGLES.items():
        if abs(angle_diff - angle) <= ASPECT_ORB:
            return name
    return None

def local_to_ut(hour: int, minute: int, utc_offset: float) -> float:
    """
    Convert local time and UTC offset to Universal Time (decimal hours).
    utc_offset in hours (e.g., -8 for PST).
    """
    ut = hour - utc_offset + (minute / 60.0)
    return ut % 24

@lru_cache(maxsize=128)
def get_julian_day(year: int, month: int, day: int, hour: int = 12, minute: int = 0, second: int = 0, timezone: str = 'UTC') -> float:
    """Calculate Julian Day from date/time and timezone."""
    tz = pytz.timezone(timezone)
    dt = datetime(year, month, day, hour, minute, second)
    dt_utc = tz.localize(dt).astimezone(pytz.utc)
    jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour + dt_utc.minute / 60 + dt_utc.second / 3600)
    return jd

def calculate_planet_positions(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    lat: float,
    lon: float,
    alt: float = 0.0,
    utc_offset: Optional[float] = None,
    ephe_path: Optional[str] = None,
    flags: int = swe.FLG_SWIEPH | swe.FLG_SPEED
) -> Dict[str, Dict[str, float]]:
    """
    Calculate planetary positions using Swiss Ephemeris.

    If utc_offset provided, local time is converted to UT automatically.

    Returns dict with planet names and positions (longitude, latitude, distance_au).
    """
    if ephe_path:
        swe.set_ephe_path(ephe_path)
        logger.info(f"Ephemeris path set: {ephe_path}")

    # Convert local time to UT
    if utc_offset is not None:
        ut = local_to_ut(hour, minute, utc_offset)
    else:
        ut = hour + minute / 60.0

    jd_ut = swe.julday(year, month, day, ut)
    swe.set_topo(lon, lat, alt)

    positions = {}
    for name, pid in PLANETS.items():
        pos, _ = swe.calc_ut(jd_ut, pid, flags)
        positions[name] = {
            "longitude": round(normalize_angle(pos[0]), 6),
            "latitude": round(pos[1], 6),
            "distance_au": round(pos[2], 8)
        }
    return positions

# --- Example Usage ---
if __name__ == "__main__":
    # Example birth data and location
    year, month, day = 1987, 5, 8
    hour, minute = 2,45 
    latitude, longitude = 34.05, -118.25  # Los Angeles approx
    utc_offset = -7  # PDT daylight saving offset
    
    # Get Sun sign by birth date
    sun_sign = get_sun_sign(month, day)
    print(f"Sun sign for {month}/{day}: {sun_sign}")
    
    # Get Julian Day for the birth time and timezone
    jd = get_julian_day(year, month, day, hour, minute, timezone='America/Los_Angeles')
    print(f"Julian Day: {jd}")
    
    # Calculate planet positions
    positions = calculate_planet_positions(year, month, day, hour, minute, latitude, longitude, utc_offset=utc_offset)
    print("Planetary Positions:")
    for planet, pos in positions.items():
        sign = degree_to_sign(pos["longitude"])
        print(f"  {planet}: {pos['longitude']}° in {sign}")

    # Example: aspect between Sun and Moon
    sun_lon = positions["Sun"]["longitude"]
    moon_lon = positions["Moon"]["longitude"]
    aspect = calculate_aspect(abs(sun_lon - moon_lon))
    print(f"Aspect between Sun and Moon: {aspect or 'None'}")
