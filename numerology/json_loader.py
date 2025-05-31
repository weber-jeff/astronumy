import json
import os
import glob # For finding files matching a pattern

class MeaningsLoader:
    def __init__(self, base_path: str):
        """
        Initialize with the base directory path where your JSON meaning files are stored.
        Example: '/path/to/json/meanings'
        """
        if not os.path.isdir(base_path):
            raise ValueError(f"Invalid meanings path: {base_path}")
        self.base_path = base_path

    def load_meaning_by_filename(self, filename: str) -> dict: # Renamed for clarity
        """
        Load and return the parsed JSON content from a specific file.
        """
        file_path = os.path.join(self.base_path, filename)
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Meaning file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in file {filename}: {e}")

    def load_all_meanings_from_directory(self) -> dict:
        """
        Loads all .json files from the base_path directory.
        Returns a dictionary where keys are filenames (without .json)
        and values are the parsed JSON content.
        """
        all_meanings = {}
        json_files = glob.glob(os.path.join(self.base_path, "*.json"))
        
        if not json_files:
            print(f"Warning: No JSON files found in {self.base_path}")
            return {}

        for file_path in json_files:
            filename_with_ext = os.path.basename(file_path)
            filename_without_ext = os.path.splitext(filename_with_ext)[0]
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    all_meanings[filename_without_ext] = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Warning: Invalid JSON in file {filename_with_ext}: {e}. Skipping this file.")
            except Exception as e:
                print(f"Warning: Could not load file {filename_with_ext}: {e}. Skipping this file.")
        return all_meanings

if __name__ == "__main__":
    print("Testing MeaningsLoader...")
    # Assuming your data files are in a 'data' subdirectory relative to this script
    # e.g., ../numerology/data/
    # Construct the path to the 'data' directory relative to this script's location
    current_script_dir = os.path.dirname(__file__)
    data_dir_path = os.path.join(current_script_dir, "data")

    print(f"Attempting to load meanings from: {data_dir_path}")

    try:
        loader = MeaningsLoader(data_dir_path)

        # Test loading a single file
        print("\n--- Loading single file (expression_meanings.json) ---")
        expression_data = loader.load_meaning_by_filename("expression_meanings.json")
        if expression_data:
            print(f"Successfully loaded expression_meanings.json. Found {len(expression_data)} entries.")
            print(f"Example entry for '1': {expression_data.get('1', 'Not found')}")

        # Test loading all files from the directory
        print("\n--- Loading all meanings from directory ---")
        all_data = loader.load_all_meanings_from_directory()
        print(f"Found {len(all_data)} meaning sets in the directory.")
        if "life_path_meanings" in all_data:
            print(f"Example: 'life_path_meanings' data for '1': {all_data['life_path_meanings'].get('1', 'Not found')}")

    except ValueError as ve:
        print(f"Error initializing loader: {ve}")
    except FileNotFoundError as fnfe:
        print(f"Error loading file: {fnfe}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
