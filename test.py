from typing import Iterable


# function to calculate average of a list of numbers
def calculate_average(numbers: Iterable[float]) -> float:
    """Calculate the average value of a sequence of numbers.

    Args:
        numbers: An iterable of numeric values.

    Returns:
        The average of the numbers, or 0.0 when the iterable is empty.
    """
    numbers_list = list(numbers)
    if len(numbers_list) == 0:
        return 0.0
    total = sum(numbers_list)
    average = total / len(numbers_list)
    return average

    