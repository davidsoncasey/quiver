import unittest

import sympy

from plot_equation import FieldPlotter


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

if __name__ == '__main__':
    unittest.main()