from __future__ import division
import re
from math import sqrt
import multiprocessing
import Queue

import sympy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

class DiffEquation(object):
    '''
    Class that contains equation information and, if the equation is valid,
    prepares the plot.
    '''
    def __init__(self, equation_string):
        self.equation_string = equation_string
        self.equation = None
        self.compute_func = None
        self.figure = None
    
    def regex_check(self):
        '''A quick regular expression check to see that the input resembles an equation'''
        match1 = re.match('^(([xy+\-*/()0-9. ]+|sin\(|cos\(|exp\(|log\()?)+$', self.equation_string)
        match2 = re.match('^.*([xy]) *([xy]).*$', self.equation_string)
        if match1 and not match2:
            return True
        return False
    
    def prep_equation(self):
        '''
        Attempt to convert the string to a SymPy function.
        From there, use lambdify to generate a function that is efficient to compute
        numerically.
        '''
        if self.regex_check():
            q = multiprocessing.Queue()
            def prep(conn):
                try:
                    equation = sympy.sympify(self.equation_string)
                    q.put(equation)
                except sympy.SympifyError:
                    pass
            
            p = multiprocessing.Process(target=prep, args=(q,))
            p.start()
            
            # See if we can get the equation within 5 seconds
            try:
                equation = q.get(timeout=5)
            except Queue.Empty:
                equation = None
            q.close()
            
            # If the process is still running, kill it
            if p.is_alive():
                p.terminate()
                p.join()
            
            if equation:    
                self.equation = equation
                x, y = sympy.symbols('x,y')
                compute_func = sympy.utilities.lambdify((x, y), self.equation)
                self.compute_func = compute_func
    
    def make_plot(self):
        '''Draw the plot on the figure attribute'''
        if self.compute_func:
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
                        dy = self.compute_func(a, b)
                        n = sqrt(dx + dy**2)
                        dy /= sqrt(n)
                        dx /= sqrt(n)
                        U[j][i] = dx
                        V[j][i] = dy
                    except (ValueError, ZeroDivisionError):
                        pass
            
            # Plot the values
            self.figure = plt.Figure()
            axes = self.figure.add_subplot(1,1,1)
            axes.quiver(X, Y, U, V, angles='xy')
            axes.axhline(color='black')
            axes.axvline(color='black')
            latex = sympy.latex(self.equation)
            axes.set_title(r'Direction field for $\frac{dy}{dx} = %s$' % latex, y=1.01)
    
    def write_data(self, output):
        '''Write the data out as base64 binary'''
        if self.figure:
            canvas = FigureCanvas(self.figure)
            self.figure.savefig(output, format='png', bbox_inches='tight')
            output.seek(0)
            return output.getvalue()
        return None
