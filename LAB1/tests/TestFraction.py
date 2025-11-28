from src.Fraction import Fraction
import unittest

class TestFraction(unittest.TestCase):
    def test_add_two_proper_fractions_returns_reduced_sum(self):
        f1 = Fraction(1, 2)
        f2 = Fraction(1, 3)
        self.assertEqual(f1 + f2, Fraction(5, 6))

    def test_subtract_two_proper_fractions_returns_reduced_difference(self):
        f1 = Fraction(1, 2)
        f2 = Fraction(1, 3)
        self.assertEqual(f1 - f2, Fraction(1, 6))

    def test_multiply_two_fractions_returns_reduced_product(self):
        f1 = Fraction(2, 3)
        f2 = Fraction(3, 4)
        self.assertEqual(f1 * f2, Fraction(1, 2))

    def test_divide_two_fractions_returns_reduced_quotient(self):
        f1 = Fraction(1, 2)
        f2 = Fraction(1, 3)
        self.assertEqual(f1 / f2, Fraction(3, 2))

    def test_equality_equivalent_fractions_are_equal(self):
        f1 = Fraction(2, 4)
        f2 = Fraction(1, 2)
        self.assertTrue(f1 == f2)

    def test_inequality_different_fractions_are_not_equal(self):
        f1 = Fraction(1, 2)
        f2 = Fraction(2, 3)
        self.assertTrue(f1 != f2)

    def test_greater_than_true_for_larger_fraction(self):
        f1 = Fraction(3, 4)
        f2 = Fraction(2, 3)
        self.assertTrue(f1 > f2)

    def test_less_than_true_for_smaller_fraction(self):
        f1 = Fraction(1, 2)
        f2 = Fraction(3, 4)
        self.assertTrue(f1 < f2)

    def test_greater_equal_true_for_equal_fractions(self):
        f1 = Fraction(5, 3)
        f2 = Fraction(5, 3)
        self.assertTrue(f1 >= f2)

    def test_less_equal_true_for_smaller_or_equal(self):
        f1 = Fraction(1, 2)
        f2 = Fraction(3, 4)
        self.assertTrue(f1 <= f2)

    def test_constructor_raises_on_zero_denominator(self):
        with self.assertRaises(ValueError):
            Fraction(1, 0)

    def test_negative_numerator_is_preserved(self):
        f = Fraction(-1, 2)
        self.assertEqual(f.num, -1)

    def test_negative_denominator_is_preserved_and_num_unchanged(self):
        f = Fraction(1, -2)
        self.assertEqual(f.den, -2)
        self.assertEqual(f.num, 1)

    def test_whole_part_for_positive_improper_fraction(self):
        f = Fraction(7, 3)
        self.assertEqual(f.whole_part, 2)

    def test_float_repr_for_half(self):
        f = Fraction(1, 2)
        self.assertEqual(f.float_repr, 0.5)

    def test_add_with_negative_fraction(self):
        f1 = Fraction(1, 2)
        f2 = Fraction(-1, 3)
        self.assertEqual(f1 + f2, Fraction(1, 6))

    def test_subtract_with_negative_fraction(self):
        f1 = Fraction(1, 2)
        f2 = Fraction(-1, 3)
        self.assertEqual(f1 - f2, Fraction(5, 6))

    def test_multiply_with_negative_fraction(self):
        f1 = Fraction(1, 2)
        f2 = Fraction(-3, 4)
        self.assertEqual(f1 * f2, Fraction(-3, 8))

    def test_divide_by_negative_fraction(self):
        f1 = Fraction(1, 2)
        f2 = Fraction(-1, 3)
        self.assertEqual(f1 / f2, Fraction(-3, 2))

    def test_whole_number_fraction_denominator_one_properties(self):
        f = Fraction(5, 1)
        self.assertEqual(f.num, 5)
        self.assertEqual(f.den, 1)

    def test_reduced_form_equality(self):
        f1 = Fraction(1, 2)
        f2 = Fraction(2, 4)
        self.assertEqual(f1, f2)

    def test_auto_reduction_on_creation(self):
        f = Fraction(4, 8)
        self.assertEqual(f, Fraction(1, 2))

    def test_repr_format_is_fraction_constructor_style(self):
        f = Fraction(1, 2)
        self.assertEqual(repr(f), "Fraction(1, 2)")

    def test_str_format_is_numerator_slash_denominator(self):
        f = Fraction(3, 4)
        self.assertEqual(str(f), "3/4")

    def test_zero_numerator_normalizes_to_denominator_one(self):
        self.assertEqual(Fraction(0, 5), Fraction(0, 1))

    def test_constructor_type_validation_raises_typeerror(self):
        with self.assertRaises(TypeError):
            Fraction("1", 2)
        with self.assertRaises(TypeError):
            Fraction(1, "2")

    def test_compare_fraction_with_int_equality_and_ordering(self):
        f = Fraction(3, 1)
        self.assertTrue(f == 3)
        self.assertTrue(f >= 3)
        self.assertTrue(f <= 3)

    def test_sign_normalization_cases(self):
        self.assertEqual(Fraction(-3, -4), Fraction(3, 4))
        self.assertEqual(Fraction(-3, 4), Fraction(-3, 4))

    def test_int_plus_fraction_right_addition(self):
        self.assertEqual(2 + Fraction(1, 3), Fraction(7, 3))

    def test_fraction_plus_int_left_addition(self):
        self.assertEqual(Fraction(1, 3) + 2, Fraction(7, 3))

    def test_int_minus_fraction_left_subtraction(self):
        self.assertEqual(1 - Fraction(1, 3), Fraction(2, 3))

    def test_fraction_minus_int_right_subtraction(self):
        self.assertEqual(Fraction(1, 3) - 1, Fraction(-2, 3))

    def test_int_times_fraction_left_multiplication(self):
        self.assertEqual(3 * Fraction(1, 4), Fraction(3, 4))

    def test_fraction_times_int_right_multiplication(self):
        self.assertEqual(Fraction(1, 4) * 3, Fraction(3, 4))

    def test_int_divided_by_fraction_left_true_division(self):
        self.assertEqual(1 / Fraction(1, 2), Fraction(1, 1))

    def test_fraction_divided_by_int_right_true_division(self):
        self.assertEqual(Fraction(1, 2) / 2, Fraction(1, 4))

    def test_mutating_num_and_den_properties_triggers_reduction(self):
        f = Fraction(4, 6)
        f.num = 10
        self.assertEqual(f, Fraction(10, 3))
        f.den = 12
        self.assertEqual(f, Fraction(10, 12))

    def test_setters_type_and_value_validation(self):
        f = Fraction(1, 2)
        with self.assertRaises(TypeError):
            f.num = 1.5
        with self.assertRaises(TypeError):
            f.den = "3"
        with self.assertRaises(ValueError):
            f.den = 0

    def test_rich_comparisons_with_ints(self):
        self.assertTrue(Fraction(5, 2) > 2)
        self.assertTrue(Fraction(3, 2) >= 1)
        self.assertTrue(Fraction(1, 2) < 1)
        self.assertTrue(Fraction(1, 2) <= 1)

    def test_whole_part_for_negative_improper_fraction(self):
        self.assertEqual(Fraction(-3, 2).whole_part, -2)

    def test_float_repr_for_negative_fraction(self):
        self.assertEqual(Fraction(-3, 2).float_repr, -1.5)

    def test_operations_with_floats_raise_typeerror(self):
        f = Fraction(1, 2)
        with self.assertRaises(TypeError):
            _ = f + 0.5
        with self.assertRaises(TypeError):
            _ = 0.5 + f
        with self.assertRaises(TypeError):
            _ = f - 0.5
        with self.assertRaises(TypeError):
            _ = 0.5 - f
        with self.assertRaises(TypeError):
            _ = f * 0.5
        with self.assertRaises(TypeError):
            _ = 0.5 * f
        with self.assertRaises(TypeError):
            _ = f / 0.5
        with self.assertRaises(TypeError):
            _ = 0.5 / f

    def test_large_fraction_reduction(self):
        self.assertEqual(Fraction(1000, 2500), Fraction(2, 5))

if __name__ == "__main__":
    unittest.main()
