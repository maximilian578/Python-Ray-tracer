from math import isinf


def isninf(value):
    return (value < 0) and isinf(value)
