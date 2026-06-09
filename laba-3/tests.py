import unittest
import tkinter as tk
from laba3 import NumberSystemCalculator

class TestNumberSystemCalculator(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.calc = NumberSystemCalculator(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_tc01_division_success_dec(self):
        val1 = int("12", 10)
        val2 = int("3", 10)
        res = self.calc.execute_math_division(val1, val2)
        self.assertEqual(self.calc.format_output(res, 10    ), "4")

    def test_tc02_division_with_remainder_dec(self):
        val1 = int("5", 10)
        val2 = int("2", 10)
        res = self.calc.execute_math_division(val1, val2)
        self.assertEqual(self.calc.format_output(res, 10), "2")

    def test_tc03_division_bin(self):
        val1 = int("1100", 2)
        val2 = int("11", 2)
        res = self.calc.execute_math_division(val1, val2)
        self.assertEqual(self.calc.format_output(res, 2), "100")

    def test_tc04_division_hex(self):
        val1 = int("FF", 16)
        val2 = int("10", 16)
        res = self.calc.execute_math_division(val1, val2)
        self.assertEqual(self.calc.format_output(res, 16), "F")

    def test_tc05_division_negative_oct(self):
        val1 = int("-14", 8)
        val2 = int("2", 8)
        res = self.calc.execute_math_division(val1, val2)
        self.assertEqual(self.calc.format_output(res, 8), "-6")

    def test_tc06_division_zero_dividend(self):
        val1 = int("0", 10)
        val2 = int("5", 10)
        res = self.calc.execute_math_division(val1, val2)
        self.assertEqual(self.calc.format_output(res, 10), "0")

    def test_tc07_dividend_less_than_divisor_bin(self):
        val1 = int("1", 2)
        val2 = int("10", 2)
        res = self.calc.execute_math_division(val1, val2)
        self.assertEqual(self.calc.format_output(res, 2), "0")

    def test_tc08_large_numbers_dec(self):
        val1 = int("999999999", 10)
        val2 = int("1", 10)
        res = self.calc.execute_math_division(val1, val2)
        self.assertEqual(self.calc.format_output(res, 10), "999999999")

    def test_tc09_zero_division_exception_dec(self):
        val1 = int("5", 10)
        val2 = int("0", 10)
        with self.assertRaises(ZeroDivisionError):
            self.calc.execute_math_division(val1, val2)

    def test_tc10_zero_division_exception_bin(self):
        val1 = int("1100", 2)
        val2 = int("0", 2)
        with self.assertRaises(ZeroDivisionError):
            self.calc.execute_math_division(val1, val2)

    def test_tc11_type_error_string(self):
        with self.assertRaises(TypeError):
            self.calc.execute_math_division("12", 3)

    def test_tc12_type_error_list(self):
        with self.assertRaises(TypeError):
            self.calc.execute_math_division(12, [3])

if __name__ == "__main__":
    unittest.main()