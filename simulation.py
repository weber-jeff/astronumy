import os
import datetime
import random

# You need to import these from your main app or modules
from data_io import load_user_feedback, save_user_feedback

# Import your actual calculation functions
from numerology.in_core_numerology.personal import get_numerological_insights
from astrology.core_astrology.traits import get_astrological_influences

def simulate_feedback_data(num_entries=10):
    if os.path.exists(load_user_feedback.USER_DATA_FILE) and os.path.getsize(load_user_feedback.USER_DATA_FILE) > 0:
        print(f"INFO (simulate_feedback_data): Using existing data from {load_user_feedback.USER_DATA_FILE}")
        return

    print(f"INFO (simulate_feedback_data): Simulating {num_entries} feedback entries...")
    start_date = datetime.date.today() - datetime.timedelta(days=num_entries)
    activities = ["Work Project", "Relationship Talk", "Health Routine", "Creative Pursuits"]
    outcomes = ["Positive", "Neutral", "Negative"]
    dummy_birth_details = {
        "birth_year": 1990,
        "birth_month": 5,
        "birth_day": 20,
        "birth_hour": 10,
        "birth_minute": 15,
        "birth_lon": -74.0060,
        "birth_lat": 40.7128,
        "birth_timezone": "America/New_York"
    }

    for i in range(num_entries):
        current_date = start_date + datetime.timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")
        numerology = get_numerological_insights(dummy_birth_details["birth_month"], dummy_birth_details["birth_day"], current_date)
        astrology = get_astrological_influences(dummy_birth_details, current_date)
        save_user_feedback(date_str, numerology, astrology, random.choice(activities), random.choice(outcomes), "Simulated entry")
    print(f"INFO (simulate_feedback_data): Finished simulating {num_entries} data entries.")
