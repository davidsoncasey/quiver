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

if __name__ == '__main__':
    unittest.main()