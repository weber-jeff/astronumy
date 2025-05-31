import os
import json
import datetime

USER_DATA_FILE = "daily_user_feedback.json"

def load_user_feedback(file_path=USER_DATA_FILE):
    if not os.path.exists(file_path):
        print(f"INFO (load_user_feedback): Feedback file not found: {file_path}")
        return []
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            if not content.strip():
                print(f"INFO (load_user_feedback): Feedback file is empty: {file_path}")
                return []
            data = json.loads(content)
            if not isinstance(data, list):
                print(f"ERROR (load_user_feedback): Feedback file does not contain a JSON list: {file_path}")
                return []
            return data
    except json.JSONDecodeError as e:
        print(f"ERROR (load_user_feedback): Error decoding JSON: {file_path}. Details: {e}")
        return []
    except Exception as e:
        print(f"ERROR (load_user_feedback): Unexpected error loading feedback: {file_path}. Details: {e}")
        return []

def save_user_feedback(date_str: str, numerology: dict, astrology: dict, user_activity: str, outcome: str, notes: str = ""):
    all_feedback = load_user_feedback()
    astrology_snapshot_serializable = astrology.copy()
    astrology_snapshot_serializable.pop('raw_transit_aspects', None)

    new_entry = {
        "date": date_str,
        "numerology_snapshot": numerology,
        "astrology_snapshot": astrology_snapshot_serializable,
        "user_activity_category": user_activity,
        "outcome_rating": outcome,
        "user_notes": notes,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    all_feedback.append(new_entry)
    try:
        with open(USER_DATA_FILE, "w") as f:
            json.dump(all_feedback, f, indent=4)
    except IOError:
        print(f"Error: Could not save feedback to {USER_DATA_FILE}")
    except TypeError as e:
        print(f"Error serializing feedback data: {e}")
