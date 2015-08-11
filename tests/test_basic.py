import unittest

import sympy

from plot_equation import regex_check, FieldPlotter, BadInputError


class RegexCheckTestCase(unittest.TestCase):
    
    def test_variables(self):
        for symbol in ('x', 'y'):
            self.assertTrue(regex_check(symbol))
    
    def test_basic_operations(self):
        operations = ['+', '-', '*', '/', '**']
        for op in operations:
            equation_str = 'x%sy' % op
            self.assertTrue(regex_check(equation_str))
    
    def test_operations(self):
        operations = ['sin', 'cos', 'exp', 'log']
        for op in operations:
            equation_str = '%s(x)' % op
            self.assertTrue(regex_check(equation_str))
    
    def test_malformed_equations(self):
        bad_equations = [
            'z',
            'xy',
        ]
        for bad_equation in bad_equations:
            print bad_equation
            with self.assertRaises(BadInputError):
                regex_check(bad_equation)


class FieldPlotterTestCase(unittest.TestCase):
    
    def test_initialization(self):
        field_plotter_no_eq = FieldPlotter()
        self.assertFalse(field_plotter_no_eq.equation)
        
        equation = sympy.sympify('x+y')
        field_plotter_eq = FieldPlotter(equation)
        self.assertEqual(equation, field_plotter_eq.equation)
    
    def test_set_equation(self):
        plotter = FieldPlotter()
        equation = sympy.sympify('2*x + 3*y')
        plotter.set_equation(equation)
        self.assertEqual(equation, plotter.equation)
    
    def test_set_equation_from_string(self):
        equations = [
            'x',
            'y',
            'x+y',
            '2*x',
            'x*y',
        ]
        plotter = FieldPlotter()
        for equation_str in equations:
            plotter.set_equation_from_string(equation_str)
            sympy_eq = sympy.sympify(equation_str)
            self.assertEqual(plotter.equation, sympy_eq)
    
    def test_set_equation_from_string_timeout(self):
        equation_str = '9**9**9**9**9**9'
        plotter = FieldPlotter()
        plotter.set_equation_from_string(equation_str)
        self.assertIsNone(plotter.equation)
    

if __name__ == '__main__':
    unittest.main()