"""Symple Fields plotting.

This module provides tools allowing for somebody to quickly and easily
plot a direction field for a given symbolic equation. Possible uses
include plotting direction fields of first order differential equations.

"""
from __future__ import division
import re
from math import sqrt
import multiprocessing
import Queue

import sympy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


class BadInputError(Exception):
    """Error raised if an equation string does not pass regex check."""
    pass

def regex_check(equation_str):
    """A quick regular expression check to see that the input is sane
    
    Args:
      equation_str (str): String of equation to be parsed by sympify
        function. Expected to be valid Python.
    
    Raises:
      BadInputError: If input does not look safe to parse as an equation.
    """
    match1 = re.match(
        r'^(([xy+\-*/()0-9. ]+|sin\(|cos\(|exp\(|log\()?)+$',
        equation_str
    )
    match2 = re.match(r'^.*([xy]) *([xy]).*$', equation_str)
    if match1 and not match2:
        return True
    raise BadInputError('Cannot parse entered equation')

class FieldPlotter(object):
    """
    Class that contains equation information and, if the equation is valid,
    prepares the plot.
    
    Args:
      equation (sympy.core.basic.Basic): A descendent of the Sympy Basic
        class. A shortcut to initialize the instance with an equation.
    
    Attributes:
      equation (sympy.core.basic.Basic): The equation to be plotted.
      figure (matplotlib.figure.Figure): Figure on which plots are made.
    """
    def __init__(self, equation=None):
        self.equation = equation
        self.figure = None
    
    def set_equation(self, equation):
        """Set the equation to be plotted.
        
        Args:
          equation (sympy.core.basic.Basic): A descendent of the Sympy Basic
            class.
        """
        self.equation = equation
    
    def set_equation_from_string(self, equation_str, fail_silently=False,
                                 check_equation=True):
        """Set equation attribute from a string.
        
        Checks to see that the string is well-formed, and
        then uses sympy.sympify to evaluate.
        
        Args:
          equation_str (str): A string representation (in valid Python)
            of the equation to be added.
          fail_silently (bool): Whether to raise sympy.SympifyError if
            equation cannot be parsed. Useful if calling from other
            application.
          check_equation (bool): Whether or not to run regex check
            on the equation_str argument.
        """
        if check_equation:
            regex_check(equation_str)
        
        # Create Queue to allow for timeout
        q = multiprocessing.Queue()
        
        def prep(conn):
            equation, error = None, False
            try:
                equation = sympy.sympify(equation_str)
            except sympy.SympifyError:
                error = True
            q.put((equation, error))
        p = multiprocessing.Process(target=prep, args=(q,))
        p.start()
        
        # See if we can get the equation within 5 seconds
        try:
            equation, error = q.get(timeout=5)
        except Queue.Empty:
            equation, error = None, None
        q.close()
        
        # If the process is still running, kill it
        if p.is_alive():
            p.terminate()
            p.join()
        
        # Check if error was raised in sympify call.
        # If we don't want to fail silently, recall sympify to reraise error
        if error and not fail_silently:
            sympy.sympify(equation_str)
        
        self.equation = equation
    
    class MissingEquationError(Exception):
        """Error raised if equation attribute has not been set."""
        pass
    
    def make_plot(self):
        """Draw the plot on the figure attribute
        
        Uses sympy.utilities.lambdify to convert equation into
        a function that can be easily computed.
        
        Raises:
          MissingEquationError: if method is called before equation is
            attached.
        """
        if not self.equation:
            raise self.MissingEquationError('No equation attached')
        
        x, y = sympy.symbols('x,y')
        compute_func = sympy.utilities.lambdify((x, y), self.equation)
        xvals, yvals = np.arange(-10, 11, 1), np.arange(-10, 11, 1)
        X, Y = np.meshgrid(xvals, yvals)
        U, V = np.meshgrid(np.zeros(len(xvals)), np.zeros(len(yvals)))
        
        # Iterate through grid and compute function value at each point
        # If value cannot be computed, default to 0
        # If value can be computed, scale by sqrt of the magnitude
        for i, a in enumerate(xvals):
            for j, b in enumerate(yvals):
                dx = 1
                try:
                    dy = compute_func(a, b)
                    n = sqrt(dx + dy**2)
                    dy /= sqrt(n)
                    dx /= sqrt(n)
                    U[j][i] = dx
                    V[j][i] = dy
                except (ValueError, ZeroDivisionError):
                    pass
        
        # Plot the values
        self.figure = plt.Figure()
        axes = self.figure.add_subplot(1, 1, 1)
        axes.quiver(X, Y, U, V, angles='xy', color='b', edgecolors=('k',))
        axes.axhline(color='black')
        axes.axvline(color='black')
        latex = sympy.latex(self.equation)
        axes.set_title(r'Direction field for $\frac{dy}{dx} = %s$' % latex, y=1.01)
    
    def write_data(self, output):
        """Write the data out as base64 binary
        
        Args:
          output (file-like object): Output to write figure to.
        """
        if self.figure:
            canvas = FigureCanvas(self.figure)
            self.figure.savefig(output, format='png', bbox_inches='tight')
