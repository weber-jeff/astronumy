
def reduce_number(number: int, keep_master: bool = True) -> int:
    """Reduce number to single digit or master number (11,22,33)."""
    while number > 9 and (not keep_master or number not in (11, 22, 33)):
        number = sum(int(d) for d in str(number))
    return number
