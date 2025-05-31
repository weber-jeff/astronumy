import sys
sys.path.insert(0, "/media/jeff/numy/numerology_ai/numerology")
from numerology.in_core_numerology.combat1 import life_path_compatibility

def get_compatibility_meaning(num1: int, num2: int) -> str:
    """Return compatibility meaning for a pair of numbers, checking both orders."""
    pair = (num1, num2)
    reverse_pair = (num2, num1)
    if pair in life_path_compatibility:
        return life_path_compatibility[pair]
    elif reverse_pair in life_path_compatibility:
        return life_path_compatibility[reverse_pair]
    else:
        return "No specific compatibility meaning found for this pair."


n1, n2 = 7, 3
comp_text = get_compatibility_meaning(n1, n2)

print(f"\n🔮 Compatibility between Life Path {n1} and {n2}:\n{comp_text.strip()}")
