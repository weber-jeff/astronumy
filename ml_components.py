import os
import joblib # For saving and loading the model
import pandas as pd # For data manipulation
from sklearn.model_selection import train_test_split # For splitting data
from sklearn.ensemble import RandomForestClassifier # The ML algorithm
from sklearn.preprocessing import OneHotEncoder, StandardScaler # For feature scaling and encoding
from sklearn.impute import SimpleImputer # For handling missing values
from sklearn.compose import ColumnTransformer # For applying different transformations to different columns
from sklearn.pipeline import Pipeline # For chaining steps together
from sklearn.metrics import accuracy_score, classification_report # For evaluating the model
import json # For creating dummy data in the test block
import random # For generating random choices
import datetime # For generating dates

# Attempt to import shared constants and functions from astro_numerology_engine
try:
    from astro_numerology_engine import load_user_feedback, USER_DATA_FILE, MODEL_FILE
except ImportError as e:
    print(f"Warning: Could not import from astro_numerology_engine: {e}. Using placeholders.")
    USER_DATA_FILE = "daily_user_feedback.json"
    MODEL_FILE = "trained_astro_numerology_model.joblib"
    def load_user_feedback():
        print("Warning: Using placeholder load_user_feedback().")
        return [] # Simplified placeholder

# Import get_numerological_insights from utils
try:
    MODEL_FILE = "trained_astro_numerology_model.joblib"
    def load_user_feedback():
        print("Warning: Using placeholder load_user_feedback().")
        if os.path.exists(USER_DATA_FILE):
            try:
                with open(USER_DATA_FILE, 'r') as f:
                    # Handle empty or malformed JSON
                    content = f.read()
                    if not content: return []
                    return json.loads(content)
            except json.JSONDecodeError:
                print(f"Warning: {USER_DATA_FILE} contains malformed JSON.")
                return []
            except Exception as ex:
                print(f"Error loading placeholder data: {ex}")
                return []
except ImportError as e:
    print(f"Warning: Could not import get_numerological_insights from numerology.meanings.utils: {e}. Synthetic data generation may be limited.")
    # Define a placeholder if import fails
    def get_numerological_insights(birth_month, birth_day, target_date_obj):
        return {"personal_day": "Error", "personal_month": "Error", "personal_year": "Error"}
        return []

# --- ML Core Functions (load_and_preprocess_data, train_outcome_model, predict_outcome) ---
# These functions would be the same as in the version from immersive_id="ml_components_py_final_v1"
# For brevity, I will not repeat them here, but assume they are present.
# Please ensure you have the full, correct versions of these functions in your actual file.

def load_and_preprocess_data(json_file_path=USER_DATA_FILE):
    """
    Loads feedback data from the specified JSON file, flattens it,
    defines features based on snapshot data, and prepares it for machine learning.
    Returns X (features DataFrame), y (target Series), and a configured preprocessor.
    """
    raw_data = load_user_feedback()
    if not raw_data:
        print("No raw data loaded from feedback. Cannot preprocess.")
        return None, None, None

    processed_data = []
    for entry in raw_data:
        astro_snapshot = entry.get('astrology_snapshot', {})
        if not isinstance(astro_snapshot, dict): astro_snapshot = {}
        numerology_snapshot = entry.get('numerology_snapshot', {})
        if not isinstance(numerology_snapshot, dict): numerology_snapshot = {}
            
        personal_day_raw = numerology_snapshot.get('personal_day', '0')
        personal_day_val = str(personal_day_raw).split(' ')[0] if isinstance(personal_day_raw, str) else str(personal_day_raw)

        flat_entry = {
            'personal_year': numerology_snapshot.get('personal_year'),
            'personal_month': numerology_snapshot.get('personal_month'),
            'personal_day': personal_day_val,
            'transiting_moon_sign': astro_snapshot.get('transiting_moon_sign'),
            'mercury_retrograde': int(astro_snapshot.get('mercury_retrograde', 0) if pd.notna(astro_snapshot.get('mercury_retrograde')) else 0),
            'dominant_element_today': astro_snapshot.get('dominant_element_today'),
            'dominant_modality_today': astro_snapshot.get('dominant_modality_today'),
            'harmonious_transit_count': astro_snapshot.get('harmonious_transit_count'),
            'challenging_transit_count': astro_snapshot.get('challenging_transit_count'),
            'key_transit_category': astro_snapshot.get('key_transit_category'),
            'user_activity_category': entry.get('user_activity_category', entry.get('user_activity', 'Unknown')),
            'outcome_rating': entry.get('outcome_rating')
        }
        if flat_entry['outcome_rating'] is not None:
            processed_data.append(flat_entry)

    if not processed_data:
        print("No data to process after filtering for entries with an outcome_rating.")
        return None, None, None

    df = pd.DataFrame(processed_data)
    if 'outcome_rating' not in df.columns or df['outcome_rating'].isnull().all():
        print("Target variable 'outcome_rating' is missing or all nulls.")
        return None, None, None
        
    y = df['outcome_rating']
    X = df.drop('outcome_rating', axis=1)

    numerical_features = [
        'personal_year', 'personal_month', 'personal_day',
        'mercury_retrograde',
        'harmonious_transit_count', 'challenging_transit_count'
    ]
    categorical_features = [
        'transiting_moon_sign', 'dominant_element_today',
        'dominant_modality_today', 'key_transit_category',
        'user_activity_category'
    ]
    
    numerical_features = [col for col in numerical_features if col in X.columns]
    categorical_features = [col for col in categorical_features if col in X.columns]

    if not numerical_features and not categorical_features:
        print("No valid numerical or categorical features identified.")
        return X, y, None

    for col in numerical_features: X[col] = pd.to_numeric(X[col], errors='coerce')

    numerical_pipeline = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
    categorical_pipeline = Pipeline(steps=[('imputer', SimpleImputer(strategy='constant', fill_value='Unknown')), ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))])

    transformers_list = []
    if numerical_features: transformers_list.append(('num', numerical_pipeline, numerical_features))
    if categorical_features: transformers_list.append(('cat', categorical_pipeline, categorical_features))
    
    if not transformers_list:
        print("No transformers to apply.")
        return X, y, None 

    preprocessor = ColumnTransformer(transformers=transformers_list, remainder='drop')
    return X, y, preprocessor

def train_outcome_model():
    X, y, preprocessor = load_and_preprocess_data()
    if X is None or y is None or preprocessor is None or X.empty or y.empty:
        print("Model training aborted: Invalid data or preprocessor.")
        return False
    if y.nunique() < 2:
        print(f"Model training aborted: Only one class ('{y.unique()[0]}') found. Need at least two classes.")
        return False
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    except ValueError as e:
        print(f"Warning: Could not stratify train-test split: {e}. Splitting without stratification.")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'))
    ])
    try:
        print("Starting model training...")
        model_pipeline.fit(X_train, y_train)
        print("Model training complete.")
        y_pred = model_pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"\nModel Evaluation (Test Set): Accuracy: {accuracy:.4f}")
        target_names = sorted([str(cls) for cls in y.unique()])
        print("Classification Report:\n", classification_report(y_test, y_pred, target_names=target_names, zero_division=0))
        joblib.dump(model_pipeline, MODEL_FILE)
        print(f"Trained model pipeline saved to {MODEL_FILE}")
        return True
    except Exception as e:
        print(f"An error occurred during model training or saving: {e}")
        import traceback
        traceback.print_exc()
        return False

def predict_outcome(numerology: dict, astrology: dict, user_activity_category: str):
    if not os.path.exists(MODEL_FILE):
        print(f"Prediction error: Model file '{MODEL_FILE}' not found.")
        return "Model not available. Please train first.", None
    try:
        model_pipeline = joblib.load(MODEL_FILE)
        personal_day_raw = numerology.get('personal_day', '0')
        personal_day_val = str(personal_day_raw).split(' ')[0] if isinstance(personal_day_raw, str) else str(personal_day_raw)
        input_features = {
            'personal_year': [numerology.get('personal_year')],
            'personal_month': [numerology.get('personal_month')],
            'personal_day': [personal_day_val],
            'transiting_moon_sign': [astrology.get('transiting_moon_sign')],
            'mercury_retrograde': [int(astrology.get('mercury_retrograde', 0) if pd.notna(astrology.get('mercury_retrograde')) else 0)],
            'dominant_element_today': [astrology.get('dominant_element_today')],
            'dominant_modality_today': [astrology.get('dominant_modality_today')],
            'harmonious_transit_count': [astrology.get('harmonious_transit_count')],
            'challenging_transit_count': [astrology.get('challenging_transit_count')],
            'key_transit_category': [astrology.get('key_transit_category')],
            'user_activity_category': [user_activity_category]
        }
        input_df = pd.DataFrame.from_dict(input_features)
        prediction = model_pipeline.predict(input_df)[0]
        probabilities = model_pipeline.predict_proba(input_df)[0]
        classifier = model_pipeline.named_steps['classifier']
        class_labels = [str(cls) for cls in classifier.classes_]
        probability_map = {class_labels[i]: prob for i, prob in enumerate(probabilities)}
        return str(prediction), probability_map
    except Exception as e:
        print(f"An error occurred during prediction: {e}")
        import traceback
        traceback.print_exc()
        return "Prediction error occurred", None

# --- Synthetic Data Generation Helper ---
# Moved outside __main__ block so it's importable/usable by other functions
def generate_synthetic_entry(entry_date):
    """Generates a single synthetic feedback entry."""
    # Define possible values for categorical features
    moon_signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    elements = ["Fire", "Earth", "Air", "Water"]
    modalities = ["Cardinal", "Fixed", "Mutable"]
    key_categories = ["Dynamic", "Stable", "Growth", "Challenge", "Social", "Emotional", "Detailed", "Creative"]
    activity_categories = ["Work", "Personal", "Social", "Creative", "Routine", "Learning"]
    outcomes = ["Positive", "Neutral", "Negative"]

    # Dummy birth details needed for get_numerological_insights
    dummy_birth_month = random.randint(1, 12)
    dummy_birth_day = random.randint(1, 28) # Use 28 to avoid issues with month lengths

    # Numerology Snapshot (using the imported function)
    numerology_snapshot_raw = get_numerological_insights(dummy_birth_month, dummy_birth_day, entry_date)
    # Clean up the personal_day string if needed, similar to load_and_preprocess_data
    personal_day_raw = numerology_snapshot_raw.get('personal_day', '0')
    personal_day_val = str(personal_day_raw).split(' ')[0] if isinstance(personal_day_raw, str) else str(personal_day_raw)

    numerology_snapshot = {
        "personal_year": numerology_snapshot_raw.get('personal_year'),
        "personal_month": numerology_snapshot_raw.get('personal_month'),
        "personal_day": personal_day_val # Use the cleaned value
    }

    # Astrology Snapshot
    harmonious_transits = random.randint(0, 5)
    challenging_transits = random.randint(0, 3)
    mercury_retro = random.choice([True, False])

    astrology_snapshot = {
        "transiting_moon_sign": random.choice(moon_signs),
        "mercury_retrograde": mercury_retro,
        "dominant_element_today": random.choice(elements),
        "dominant_modality_today": random.choice(modalities),
        "harmonious_transit_count": harmonious_transits,
        "challenging_transit_count": challenging_transits,
        "key_transit_category": random.choice(key_categories)
    }

    # User Activity
    user_activity = random.choice(activity_categories)

    # Simulate Outcome Logic (simple logic for synthetic data)
    outcome_score = harmonious_transits - challenging_transits - (2 if mercury_retro else 0)
    if outcome_score > 1:
        outcome_rating = random.choices(outcomes, weights=[0.6, 0.3, 0.1], k=1)[0] # Higher chance of Positive
    elif outcome_score < -1:
        outcome_rating = random.choices(outcomes, weights=[0.1, 0.3, 0.6], k=1)[0] # Higher chance of Negative
    else:
        outcome_rating = random.choices(outcomes, weights=[0.3, 0.4, 0.3], k=1)[0] # Higher chance of Neutral

    return {
    "date": entry_date.strftime("%Y-%m-%d"),
    "numerology_snapshot": numerology_snapshot,
    "astrology_snapshot": astrology_snapshot,
    "user_activity_category": user_activity,
    "user_activity": user_activity + " task",
    "outcome_rating": outcome_rating,
    "notes": "Synthetic feedback entry."
}

# This block allows testing the module directly (e.g., python ml_components.py)
if __name__ == '__main__':
    print("Running ML Components Test Block...")

    # Check if USER_DATA_FILE exists and has content. If not, generate synthetic data.
    generate_new_data = False
    if not os.path.exists(USER_DATA_FILE):
        print(f"'{USER_DATA_FILE}' not found. Will generate synthetic data.")
        generate_new_data = True
    else:
        try:
            with open(USER_DATA_FILE, 'r') as f:
                existing_data = json.load(f)
                if not existing_data or len(existing_data) < 10: # Arbitrary threshold for "enough" data
                    print(f"'{USER_DATA_FILE}' is present but has insufficient data ({len(existing_data)} entries). Will generate new synthetic data.")
                    generate_new_data = True
                else:
                    print(f"Found existing data in '{USER_DATA_FILE}' ({len(existing_data)} entries). Using this data.")
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error reading '{USER_DATA_FILE}': {e}. Will generate new synthetic data.")
            generate_new_data = True
            
    if generate_new_data:
        num_entries_to_generate = 100 # Generate 100 synthetic entries
        print(f"Generating {num_entries_to_generate} synthetic feedback entries...")
        
        synthetic_feedback_data = []
        start_date = datetime.date(2023, 1, 1)
        for i in range(num_entries_to_generate):
            current_date = start_date + datetime.timedelta(days=i)
            synthetic_feedback_data.append(generate_synthetic_entry(current_date))
        
        try:
            with open(USER_DATA_FILE, 'w') as f:
                json.dump(synthetic_feedback_data, f, indent=4)
            print(f"Successfully wrote {num_entries_to_generate} synthetic entries to '{USER_DATA_FILE}'")
        except Exception as e_write:
            print(f"Error writing synthetic data to '{USER_DATA_FILE}': {e_write}")
            # Fallback to a very small in-memory list if file write fails, to allow some testing
            synthetic_feedback_data = [generate_synthetic_entry(datetime.date.today()) for _ in range(5)]

# Inside ml_components.py

# ... (all functions including generate_synthetic_entry defined above) ...

if __name__ == '__main__':
    print("Running ML Components Test Block...")

    # 1. Decide if we need to generate new synthetic data:
    generate_new_data = False
    if not os.path.exists(USER_DATA_FILE): # Check if the feedback file exists
        print(f"'{USER_DATA_FILE}' not found. Will generate synthetic data.")
        generate_new_data = True
    else:
        # If file exists, check if it's empty or has very few entries
        try:
            with open(USER_DATA_FILE, 'r') as f:
                content = f.read()
                if not content: # File is empty
                    print(f"'{USER_DATA_FILE}' is empty. Will generate synthetic data.")
                    generate_new_data = True
                else:
                    existing_data = json.loads(content) # Try to parse JSON
                    if not existing_data or len(existing_data) < 10: # Arbitrary threshold: if less than 10 entries, regenerate
                        print(f"'{USER_DATA_FILE}' has only {len(existing_data)} entries. Will generate new synthetic data.")
                        generate_new_data = True
                    else:
                        print(f"Found {len(existing_data)} existing entries in '{USER_DATA_FILE}'. Using this data.")
        except (json.JSONDecodeError, Exception) as e: # Handle errors reading or parsing the file
            print(f"Error reading or parsing '{USER_DATA_FILE}': {e}. Will generate new synthetic data.")
            generate_new_data = True
            
 
        
        synthetic_feedback_data = []
        start_date = datetime.date(2023, 1, 1) # Start generating data from this date
        for i in range(num_entries_to_generate):
            current_date = start_date + datetime.timedelta(days=i) # Increment date for each entry
            synthetic_feedback_data.append(generate_synthetic_entry(current_date))
        
        try:
            # Write the list of synthetic entries to the JSON file
            with open(USER_DATA_FILE, 'w') as f:
                json.dump(synthetic_feedback_data, f, indent=4) # indent=4 makes the JSON file human-readable
            print(f"Successfully wrote {num_entries_to_generate} synthetic entries to '{USER_DATA_FILE}'")
        except Exception as e_write:
            print(f"Error writing synthetic data to '{USER_DATA_FILE}': {e_write}")
            # As a fallback, if file writing fails, we might still want to test with a tiny bit of in-memory data
            # This part is optional and makes the script more resilient for testing even with file permission issues.
            # synthetic_feedback_data = [generate_synthetic_entry(datetime.date.today()) for _ in range(5)] 

    # 3. Attempt to train the model:
    #    train_outcome_model() will now use the data from USER_DATA_FILE,
    #    which is either your pre-existing data or the synthetic data we just generated.
    print("\n--- Attempting to Train Model ---")
    training_successful = train_outcome_model()

    # 4. If training was successful, attempt a test prediction:
    if training_successful:
        print("\n--- Attempting a Test Prediction ---")
        # Create sample input data for the predict_outcome function
        sample_numerology = {"personal_year": "7", "personal_month": "1", "personal_day": "5 (Focus)"}
        sample_astrology = {"transiting_moon_sign": "Aries", "mercury_retrograde": False, 
                            "dominant_element_today": "Fire", "harmonious_transit_count": 2, 
                            "challenging_transit_count": 1, "key_transit_category": "Dynamic"}
        sample_activity_cat = "Work" # This should be a category the model might have seen
        
        prediction, probabilities = predict_outcome(sample_numerology, sample_astrology, sample_activity_cat)
        
        
        # Inside ml_components.py

import random # For generating random choices
import datetime # For generating dates

# ... (other imports) ...

def generate_synthetic_entry(entry_date):
    """Generates a single synthetic feedback entry."""
    # 1. Define possible values for categorical features:
    #    This gives us a controlled vocabulary for our synthetic data.
    moon_signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    elements = ["Fire", "Earth", "Air", "Water"]
    modalities = ["Cardinal", "Fixed", "Mutable"]
    key_categories = ["Dynamic", "Stable", "Growth", "Challenge", "Social", "Emotional", "Detailed", "Creative"]
    activity_categories = ["Work", "Personal", "Social", "Creative", "Routine", "Learning"]
    outcomes = ["Positive", "Neutral", "Negative"] # Our target variable categories

    # 2. Randomly create a Numerology Snapshot:
    num_personal_year = str(random.randint(1, 9)) # A random single digit year
    num_personal_month = str(random.randint(1, 9))# A random single digit month
    num_personal_day_num = random.randint(1, 9)
    # Randomly decide if the personal_day string includes a meaning or is just the number
    num_personal_day = f"{num_personal_day_num} (Focus on {num_personal_day_num})" if random.choice([True, False]) else str(num_personal_day_num)

    numerology_snapshot = {
        "personal_year": num_personal_year,
        "personal_month": num_personal_month,
        "personal_day": num_personal_day # This will be cleaned by load_and_preprocess_data
    }

    # 3. Randomly create an Astrology Snapshot:
    harmonious_transits = random.randint(0, 5) # Random count
    challenging_transits = random.randint(0, 3) # Random count
    mercury_retro = random.choice([True, False]) # Randomly True or False

    astrology_snapshot = {
        "transiting_moon_sign": random.choice(moon_signs),
        "mercury_retrograde": mercury_retro,
        "dominant_element_today": random.choice(elements),
        "dominant_modality_today": random.choice(modalities),
        "harmonious_transit_count": harmonious_transits,
        "challenging_transit_count": challenging_transits,
        "key_transit_category": random.choice(key_categories)
    }

    # 4. Randomly create User Activity:
    user_activity = random.choice(activity_categories)

    # 5. Simulate Outcome Logic (This is where you can embed patterns):
    #    This is a very simple example. The goal isn't to be perfectly realistic,
    #    but to create data where *some* relationship exists between features and outcome,
    #    so we can see if the model can learn *something*.
    outcome_score = harmonious_transits - challenging_transits - (2 if mercury_retro else 0)
    # Based on the score, we'll bias the probability of Positive, Neutral, or Negative outcomes.
    if outcome_score > 1: # More harmonious, no Mercury Rx
        outcome_rating = random.choices(outcomes, weights=[0.6, 0.3, 0.1], k=1)[0] # Higher chance of Positive
    elif outcome_score < -1: # More challenging, or Mercury Rx
        outcome_rating = random.choices(outcomes, weights=[0.1, 0.3, 0.6], k=1)[0] # Higher chance of Negative
    else: # Balanced or mildly influential
        outcome_rating = random.choices(outcomes, weights=[0.3, 0.4, 0.3], k=1)[0] # Higher chance of Neutral

    # 6. Assemble and return the full synthetic entry:
    return {
        "date": entry_date.strftime("%Y-%m-%d"), # Use the passed-in date
        "numerology_snapshot": numerology_snapshot,
        "astrology_snapshot": astrology_snapshot,
        "user_activity_category": user_activity, # For simplicity, using the activity as its own category
        "user_activity": user_activity + " task", # Adding some detail for the 'user_activity' field
        "outcome_rating": outcome_rating, # The simulated outcome
        "notes": "Synthetic feedback entry." # A note indicating it's artificial
    }

        
        
    print(f"\nTest Prediction for Activity Category '{sample_activity_cat}':")
    print(f"  Predicted Outcome: {prediction}")
    if probabilities:
            # Format probabilities to be more readable (e.g., percentages)
            formatted_probs = {k: f"{v:.2%}" for k, v in probabilities.items()}
            print(f"  Probabilities: {formatted_probs}")
    else:
        print("\nSkipping test prediction because model training was not successful or data was insufficient.")
    
    print("\nML Components Test Block Finished.")



    print("\n--- Attempting to Train Model ---")
    training_successful = train_outcome_model()

    if training_successful:
        print("\n--- Attempting a Test Prediction ---")
        # Example input data for prediction (must match your daily insight structure)
        sample_numerology = {"personal_year": "7", "personal_month": "1", "personal_day": "5 (Focus)"}
        sample_astrology = {"transiting_moon_sign": "Aries", "mercury_retrograde": False, 
                            "dominant_element_today": "Fire", "harmonious_transit_count": 2, 
                            "challenging_transit_count": 1, "key_transit_category": "Dynamic"}
        sample_activity_cat = "Work"
        
        prediction, probabilities = predict_outcome(sample_numerology, sample_astrology, sample_activity_cat)
        
        print(f"\nTest Prediction for Activity Category '{sample_activity_cat}':")
        print(f"  Predicted Outcome: {prediction}")
        if probabilities:
            # Format probabilities for display
            formatted_probs = {k: f"{v:.2%}" for k, v in probabilities.items()}
            print(f"  Probabilities: {formatted_probs}")
    else:
        print("\nSkipping test prediction because model training was not successful or data was insufficient.")
    
    print("\nML Components Test Block Finished.")
