# numerology/in_core_numerology/soul_urge.py

PYTHAGOREAN_MAP = {
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5,
    "F": 6, "G": 7, "H": 8, "I": 9, "J": 1,
    "K": 2, "L": 3, "M": 4, "N": 5, "O": 6,
    "P": 7, "Q": 8, "R": 9, "S": 1, "T": 2,
    "U": 3, "V": 4, "W": 5, "X": 6, "Y": 7,  # Y included as a vowel here
    "Z": 8
}

def reduce_number(n):
    """Reduce number to a core digit or master number (11, 22, 33)."""
    while n > 9 and n not in [11, 22, 33]:
        n = sum(int(d) for d in str(n))
    return n

def calculate_soul_urge(full_name: str) -> int:
    """Calculate Soul Urge number based on vowels in the full name."""
    vowels = {"A", "E", "I", "O", "U", "Y"}  # Includes Y by default
    name = full_name.upper().replace(" ", "")
    total = sum(PYTHAGOREAN_MAP[char] for char in name if char in vowels and char in PYTHAGOREAN_MAP)
    return reduce_number(total)

# Optional: for testing when run directly
if __name__ == "__main__":
    name_input = "Jeffrey Isaac Thomas"
    result = calculate_soul_urge(name_input)
    print(f"Soul Urge Number for {name_input}: {result}")
