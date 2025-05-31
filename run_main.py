from datetime import datetime
from user_profile import UserProfile

def main():
    # User information
    user_name = "Jeff"
    user_birth_date = "1987-05-08"

    # Convert string to datetime.datetime object
    birth_datetime_obj = datetime.strptime(user_birth_date, "%Y-%m-%d")

    # Create UserProfile
    user = UserProfile(
        name=user_name,
        birthdate=birth_datetime_obj # Pass the datetime.datetime object
    )

    # (Optional) Print to confirm
    print("User profile created successfully:")
    print(user)

if __name__ == "__main__":
    main()
