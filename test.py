import unittest
import math
import validator
import function_parser
import indefinite_integral
import definite_integral

class TestIndefiniteIntegral(unittest.TestCase):
    def setUp(self):
        self.calc = lambda e: indefinite_integral.IndefiniteIntegralCalculator(e.replace('^', '**')).calculate()

    def test_basic_powers(self):
        self.assertEqual(self.calc("x^2"), "1/3x^3")
        self.assertEqual(self.calc("5"), "5x")
        self.assertEqual(self.calc("-x"), "-1/2x^2")

    def test_negative_powers(self):
        self.assertEqual(self.calc("x^-2"), "-x^-1")
        self.assertEqual(self.calc("1/x"), "ln|x|")
        self.assertEqual(self.calc("2/x^3"), "-x^-2")
        self.assertEqual(self.calc("x^-1"), "ln|x|")

    def test_sums(self):
        self.assertEqual(self.calc("x^2 + 1/x"), "1/3x^3 + ln|x|")
        self.assertEqual(self.calc("x^-2 + x + 5"), "-x^-1 + 1/2x^2 + 5x")
        res = self.calc("1/x^2 - 2/x")
        self.assertTrue(res in ["-x^-1 - 2ln|x|", "-1x^-1 - 2ln|x|"])

    def test_rational_division(self):
        self.assertEqual(self.calc("(x^2 + 1)/x"), "1/2x^2 + ln|x|")
        self.assertEqual(self.calc("(x^3 + 2x^2 + x)/x^2"), "1/2x^2 + 2x + ln|x|")
        self.assertEqual(self.calc("(5x^4 - 3)/x"), "5/4x^4 - 3ln|x|")

    def test_complex_fractions(self):
        self.assertEqual(self.calc("1/(x+1)"), "ln|x+1|")
        self.assertEqual(self.calc("3/(x-5)"), "3ln|x-5|")

class TestDefiniteIntegral(unittest.TestCase):
    def setUp(self):
        self.calc_class = definite_integral.DefiniteIntegralCalculator

    def test_simple_linear(self):
        calc = self.calc_class("x", 0, 2, 1000)
        value, err = calc.calculate()
        self.assertEqual(err, "")
        self.assertAlmostEqual(value, 2.0, places=5)

    def test_quadratic(self):
        calc = self.calc_class("x**2", 0, 3, 1000)
        value, err = calc.calculate()
        self.assertEqual(err, "")
        self.assertAlmostEqual(value, 9.0, places=5)

    def test_constant(self):
        calc = self.calc_class("5", 1, 4, 100)
        value, err = calc.calculate()
        self.assertEqual(err, "")
        self.assertAlmostEqual(value, 15.0, places=5)

    def test_rational_function(self):
        calc = self.calc_class("1/x", 1, math.e, 1000)
        value, err = calc.calculate()
        self.assertEqual(err, "")
        self.assertAlmostEqual(value, 1.0, places=4)

    def test_division_by_zero_boundary(self):
        calc = self.calc_class("1/x", 0, 1, 1000)
        value, err = calc.calculate()
        self.assertIn("Ошибка", err)

    def test_negative_interval(self):
        calc = self.calc_class("x", -2, 2, 1000)
        value, err = calc.calculate()
        self.assertAlmostEqual(value, 0.0, places=5)

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = function_parser.FunctionParser()

    def test_implicit_multiplication(self):
        self.assertEqual(self.parser.to_evaluable("2x"), "2*x")
        self.assertEqual(self.parser.to_evaluable("3(x+1)"), "3*(x+1)")
        self.assertEqual(self.parser.to_evaluable("(x+1)(x-2)"), "(x+1)*(x-2)")

    def test_power_replacement(self):
        self.assertEqual(self.parser.to_evaluable("x^2"), "x**2")
        self.assertEqual(self.parser.to_evaluable("x^-1"), "x**-1")

    def test_cyrillic_fix(self):
        self.assertEqual(self.parser.to_evaluable("х^2"), "x**2")

class TestValidator(unittest.TestCase):
    def setUp(self):
        self.val = validator.Validator()

    def test_valid_expressions(self):
        self.assertTrue(self.val.validate_function("x^2 + 1/x")[0])
        self.assertTrue(self.val.validate_function("(x+1)/(x-1)")[0])

    def test_forbidden_chars(self):
        valid, msg = self.val.validate_function("x + y")
        self.assertFalse(valid)
        self.assertIn("только от переменной x", msg)

    def test_forbidden_functions(self):
        valid, msg = self.val.validate_function("sin(x)")
        self.assertFalse(valid)
        self.assertIn("только рациональные функции", msg)

    def test_syntax_errors(self):
        valid, msg = self.val.validate_function("(x+1")
        self.assertFalse(valid)
        self.assertEqual(msg, "Ошибка синтаксиса")

    def test_sqrt_forbidden(self):
        valid, msg = self.val.validate_function("sqrt(x)")
        self.assertFalse(valid)

    def test_log_forbidden(self):
        valid, msg = self.val.validate_function("log(x)")
        self.assertFalse(valid)

    def test_empty_input(self):
        valid, msg = self.val.validate_function("")
        self.assertFalse(valid)

    def test_invalid_symbols(self):
        valid, msg = self.val.validate_function("x @ 2")
        self.assertFalse(valid)

    def test_double_operators(self):
        valid, msg = self.val.validate_function("x++2")
        self.assertFalse(valid)

if __name__ == "__main__":
    unittest.main()