from typing import Tuple


def coord_to_battleship_notation(coord: Tuple[int, int]) -> str:
    x, y = coord
    letters = "АБВГДЕЖЗИК"
    letter = letters[x]
    number = y + 1
    return f"{letter}{number}"
