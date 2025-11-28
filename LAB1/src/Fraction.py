from math import gcd
from unittest import result

class Fraction:
    """
    A class representing a fraction.

    Attributes:
        num (int): The numerator of the fraction.
        den (int): The denominator of the fraction.

    Methods:
        __init__(num, den): Initializes the fraction with a numerator and denominator.
        _reduce(): Reduces the fraction to its simplest form.
        __add__(other): Adds two fractions.
        __sub__(other): Subtracts two fractions.
        __mul__(other): Multiplies two fractions.
        __truediv__(other): Divides two fractions.
        __eq__(other): Checks if two fractions are equal.
        __ne__(other): Checks if two fractions are not equal.
        __gt__(other): Checks if the fraction is greater than another.
        __lt__(other): Checks if the fraction is less than another.
        __ge__(other): Checks if the fraction is greater than or equal to another.
        __le__(other): Checks if the fraction is less than or equal to another.
        __str__(): Returns the string representation of the fraction.
        __repr__(): Returns the detailed string representation of the fraction.
    """
    
    __slots__ = ["_num", "_den"]

    def __init__(self, num, den):
        """
        Initializes the fraction with a numerator and denominator.

        Args:
            num (int): The numerator of the fraction.
            den (int): The denominator of the fraction.

        Raises:
            TypeError: If the numerator or denominator is not an integer.
            ValueError: If the denominator is zero.
        """
        if not isinstance(num, int):
            raise TypeError("Numerator must be integer")
        if not isinstance(den, int):
            raise TypeError("Denominator must be integer")
        if den == 0:
            raise ValueError("Denominator must be non-zero")
        self._num = num
        self._den = den
        self._reduce()

    @staticmethod
    def _convert_to_fraction(value):
        """
        Converts a value to a Fraction instance.

        Args:
            value (int or Fraction): The value to be converted.

        Returns:
            Fraction: The Fraction instance corresponding to the value.

        Raises:
            TypeError: If the value is neither an integer nor a Fraction.
        """
        if isinstance(value, int):
            return Fraction(value, 1)
        if isinstance(value, Fraction):
            return value
        raise TypeError("Value must be integer or Fraction")

    def _reduce(self):
        """
        Reduces the fraction to its simplest form by dividing both the numerator
        and denominator by their greatest common divisor (gcd).
        """
        g = gcd(self.num, self.den)
        self._num //= g
        self._den //= g

    @property
    def num(self):
        """Returns the numerator of the fraction."""
        return self._num

    @property
    def den(self):
        """Returns the denominator of the fraction."""
        return self._den

    @property
    def whole_part(self):
        """
        Returns the whole part of the fraction (integer division).

        Returns:
            int: The whole part of the fraction.
        """
        return self.num // self.den

    @property
    def float_repr(self):
        """
        Returns the floating point representation of the fraction.

        Returns:
            float: The decimal equivalent of the fraction.
        """
        return self.num / self.den

    @num.setter
    def num(self, value):
        """
        Sets the numerator of the fraction and reduces it.

        Args:
            value (int): The new numerator.

        Raises:
            TypeError: If the numerator is not an integer.
        """
        if not isinstance(value, int):
            raise TypeError("Numerator must be integer")
        self._num = value
        self._reduce()

    @den.setter
    def den(self, value):
        """
        Sets the denominator of the fraction and reduces it.

        Args:
            value (int): The new denominator.

        Raises:
            TypeError: If the denominator is not an integer.
            ValueError: If the denominator is zero.
        """
        if not isinstance(value, int):
            raise TypeError("Denominator must be integer")
        if value == 0:
            raise ValueError("Denominator must be non-zero")
        self._den = value
        self._reduce()

    def __add__(self, other):
        """
        Adds two fractions.

        Args:
            other (Fraction): The fraction to be added.

        Returns:
            Fraction: The result of the addition.
        """
        other = self._convert_to_fraction(other)
        return Fraction(
            self.num * other.den + other.num * self.den, self.den * other.den
        )

    def __radd__(self, other):
        """
        Reversed addition (for when the fraction is the second operand).

        Args:
            other (Fraction): The fraction to be added.

        Returns:
            Fraction: The result of the addition.
        """
        return self.__add__(other)

    def __sub__(self, other):
        """
        Subtracts two fractions.

        Args:
            other (Fraction): The fraction to be subtracted.

        Returns:
            Fraction: The result of the subtraction.
        """
        other = self._convert_to_fraction(other)
        return Fraction(
            self.num * other.den - other.num * self.den, self.den * other.den
        )

    def __rsub__(self, other):
        """
        Reversed subtraction (for when the fraction is the second operand).

        Args:
            other (Fraction): The fraction to be subtracted.

        Returns:
            Fraction: The result of the subtraction.
        """
        other = self._convert_to_fraction(other)
        return Fraction(
            other.num * self.den - self.num * other.den, self.den * other.den
        )

    def __mul__(self, other):
        """
        Multiplies two fractions.

        Args:
            other (Fraction): The fraction to be multiplied.

        Returns:
            Fraction: The result of the multiplication.
        """
        other = self._convert_to_fraction(other)
        return Fraction(self.num * other.num, self.den * other.den)

    def __rmul__(self, other):
        """
        Reversed multiplication (for when the fraction is the second operand).

        Args:
            other (Fraction): The fraction to be multiplied.

        Returns:
            Fraction: The result of the multiplication.
        """
        return self.__mul__(other)

    def __truediv__(self, other):
        """
        Divides two fractions.

        Args:
            other (Fraction): The fraction to be divided.

        Returns:
            Fraction: The result of the division.
        """
        other = self._convert_to_fraction(other)
        return Fraction(self.num * other.den, self.den * other.num)

    def __rtruediv__(self, other):
        """
        Reversed division (for when the fraction is the second operand).

        Args:
            other (Fraction): The fraction to divide by.

        Returns:
            Fraction: The result of the division.
        """
        other = self._convert_to_fraction(other)
        return Fraction(other.num * self.den, self.den * other.num)

    def __eq__(self, other):
        """
        Checks if two fractions are equal.

        Args:
            other (Fraction): The fraction to compare.

        Returns:
            bool: True if the fractions are equal, False otherwise.
        """
        other = self._convert_to_fraction(other)
        return self.num*other.den== self.den*other.num

    def __ne__(self, other):
        """
        Checks if two fractions are not equal.

        Args:
            other (Fraction): The fraction to compare.

        Returns:
            bool: True if the fractions are not equal, False otherwise.
        """
        other = self._convert_to_fraction(other)
        return self.num * other.den != other.num * self.den

    def __gt__(self, other):
        """
        Checks if the fraction is greater than another.

        Args:
            other (Fraction): The fraction to compare.

        Returns:
            bool: True if the fraction is greater, False otherwise.
        """
        other = self._convert_to_fraction(other)
        return self.num * other.den > other.num * self.den

    def __ge__(self, other):
        """
        Checks if the fraction is greater than or equal to another.

        Args:
            other (Fraction): The fraction to compare.

        Returns:
            bool: True if the fraction is greater than or equal to the other, False otherwise.
        """
        other = self._convert_to_fraction(other)
        return self.num * other.den >= other.num * self.den

    def __lt__(self, other):
        """
        Checks if the fraction is less than another.

        Args:
            other (Fraction): The fraction to compare.

        Returns:
            bool: True if the fraction is less, False otherwise.
        """
        other = self._convert_to_fraction(other)
        return self.num * other.den < other.num * self.den

    def __le__(self, other):
        """
        Checks if the fraction is less than or equal to another.

        Args:
            other (Fraction): The fraction to compare.

        Returns:
            bool: True if the fraction is less than or equal to the other, False otherwise.
        """
        other = self._convert_to_fraction(other)
        return self.num * other.den <= other.num * self.den

    def __str__(self):
        """
        Returns the string representation of the fraction.

        Returns:
            str: The fraction as a string in the form 'numerator/denominator'.
        """
        return f"{self.num}/{self.den}"

    def __repr__(self):
        """
        Returns a detailed string representation of the fraction.

        Returns:
            str: The fraction as a string in the form 'Fraction(numerator, denominator)'.
        """
        return f"Fraction({self.num}, {self.den})"

