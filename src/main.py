# app.py

def add_numbers(a, b):
    """
    Returns the sum of two numbers.
    Raises:
        TypeError: If inputs are not int or float.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be int or float")
    return a + b
print("Hello World!")
