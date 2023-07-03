# Functions for bit manipulation
# Useful for representing DP states using a single integer
# NOTE: S will be the name of the parameter which represents the integer bit set
# NOTE: 0 based indexing is used throughout

# ==============================================================================

# CHECKS

def isBitOn(S: int, j: int) -> bool:
    """
    Checks whether the jth bit is on
    """
    return (S & (1<<j))

def isBitOff(S: int, j: int) -> bool:
    """
    Checks whether the jth bit is off
    """
    return not (S & (1<<j))

def isPowerOfTwo(S: int) -> bool:
    """
    Checks whether S is a power of 2
    """
    return not (S & (S - 1))

# ==============================================================================

# OPERATIONS

def setBit(S: int, j: int) -> int:
    """
    Sets the jth bit to 1, regardless of its original state
    """
    return (S | (1<<j))

def clearBit(S: int, j: int) -> int:
    """
    Clears the jth bit to 0, regardless of its original state
    """
    return (S & (~(1<<j)))

def flipBit(S: int, j: int) -> int:
    """
    Flips the jth bit, 1 -> 0, 0 -> 1
    """
    return (S ^ (1<<j))

def turnOnLastZero(S: int) -> int:
    """
    Turns the last off bit on, if all bits are on then adds 1
    """
    return ((S) | (S + 1))

def turnOffLastOne(S: int) -> int:
    """
    Turns the last on bit off, if all bits are off then returns 0
    """
    return (S & (S - 1))

def turnOnLastConsecutiveZeroes(S: int) -> int:
    """
    Turns the last consecutive off bits on, if all bits are on then returns original number
    """
    return ((S) | (S - 1))

def turnOffLastConsecutiveOnes(S: int) -> int:
    """
    Turns the last consecutive on bits off, if all bits are off then returns 0
    """
    return ((S) & (S + 1))

# ==============================================================================

# GETTERS

def smallestBitOn(S: int) -> int:
    """
    Returns the smallest bit that is on
    """
    return (S & (-S))

def smallestBitOff(S: int) -> int:
    """
    Returns the smallest bit that is off
    """
    return ((~S) & (-(~S)))

# Python has the following built-in functions
# - int.bit_length(), which returns the number of bits an integer has
# - int.bit_count(), which returns the number of bits that are on i.e. 1s

def setAllBitsOn(n: int) -> int:
    """
    Returns a bit set of length n with all bits on
    """
    return (1<<n)-1

from math import log2

def nearestPowerOfTwo(S: int) -> int:
    """
    Returns the nearest power of 2
    """
    return 1<<round(log2(S))

def nextPowerOfTwo(S: int) -> int:
    """
    Returns the next power of 2
    """
    return 1<<S.bit_length()

def previousPowerOfTwo(S: int) -> int:
    """
    Returns the previous power of 2
    """
    return 1<<(S.bit_length()-2)
