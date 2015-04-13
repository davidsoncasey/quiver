from __future__ import division
import re
import StringIO
import base64
from math import sqrt
from flask import Flask, render_template, request, make_response
from sympy import sympify, SympifyError
from sympy.utilities.lambdify import lambdify
from sympy.abc import x, y
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)

@app.route('/')
def quiver():
    return render_template('quiver.html')

def prep_equation(equation_string):
    # First do a regualar expression check to verify that they've actually entered an equation
    match1 = re.match('^(([xy+\-*/()0-9. ]+|sin|cos|exp|log)?)+$', equation_string)
    match2 = re.match('^.*([xy]) *([xy]).*$', equation_string)
    if match1 and not match2:
        try:
            equation = sympify(equation_string)
            f = lambdify((x, y), equation)
            return f
        except SympifyError:
            pass
    return None

@app.route('/plot/', methods=['GET',])
def plot():
    equation_string = request.args.get('equation')
    f = prep_equation(equation_string)
    
    # If the equation is valid, compute the values for each value in the grid
    if f:
        xvals, yvals = np.arange(-10, 11, 1), np.arange(-10, 11, 1)
        X, Y = np.meshgrid(xvals, yvals)
        U, V = np.meshgrid(np.zeros(len(xvals)), np.zeros(len(yvals)))
        for i, a in enumerate(xvals):
            for j, b in enumerate(yvals):
                dx = 1
                try:
                    dy = f(a, b)
                    n = sqrt(dx + dy**2)
                    dx /= n
                    dy /= n
                    U[j][i] = dx        
                    V[j][i] = dy
                except (ValueError, ZeroDivisionError):
                    pass
        
        # Plot the values
        fig = plt.Figure()
        axis = fig.add_subplot(1,1,1)
        axis.quiver(X, Y, U, V)
        
        # Write output to memory and add to response object
        output = StringIO.StringIO()
        canvas = FigureCanvas(fig)
        fig.savefig(output, format='png')
        output.seek(0)
        response = make_response(base64.b64encode(output.getvalue()))
        response.mimetype = 'image/png'
        return response
    else:
        return make_response('')

if __name__ == '__main__':
    app.run(debug=True)