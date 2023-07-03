"""
Python has built-in support for bin, hex, and oct
"{0:b}".format(100) # bin: 1100100
"{0:x}".format(100) # hex: 64
"{0:o}".format(100) # oct: 144
"""


def changeBase(digit_list: list[int], tobase: int, frombase: int = 10) -> list[int]:
    """
    A function for converting a number, represented in the form of a digit list,
    into any other base, and returns the new digit list
    """
    number = sum(digit_list[-i-1]*(frombase**i) for i in range(len(digit_list)-1, -1, -1)) # convert to decimal
    if number == 0:
        return [0]
    new_digits = []
    while number:
        new_digits.append(int(number % tobase))
        number //= tobase
    return new_digits[::-1]

def decimal_to_digit_list(number: int):
    """
    Converts a decimal number into a list of digits
    """
    return [int(digit) for digit in str(number)]



# print(changeBase(decimal_to_digit_list(67854 ** 15 - 102), 577))
# Correctly outputs:
# [4, 473, 131, 96, 431, 285, 524, 486, 28, 23, 16, 82, 292, 538, 149, 25, 41, 483, 100, 517, 131, 28, 0, 435, 197, 264, 455]
