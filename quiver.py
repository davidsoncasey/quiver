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

@app.route('/plot/', methods=['GET', 'POST'])
def plot():
    equation = None
    equation_string = request.args.get('equation')
    
    # See if the input passes a basic regular expression check
    m = re.match('^([xy+\-*/()0-9. ]+|sin|cos|exp|log)+$', equation_string)
    
    # If the input passes first check, create a SymPy equation and plot a vector field
    if m:
        try:
            equation = sympify(equation_string)
            f = lambdify((x, y), equation)
            xvals, yvals = np.arange(-10, 11, 1), np.arange(-10, 11, 1)
            X, Y = np.meshgrid(xvals, yvals)
            U, V = np.meshgrid(np.ones(len(xvals)), np.zeros(len(yvals)))
            for i, a in enumerate(xvals):
                for j, b in enumerate(yvals):
                    dx = 1
                    try:
                        dy = f(a, b)
                        n = sqrt(dx + dy**2)
                        dx /= n
                        dy /= n
                    except ValueError, ZeroDivisionError:
                        dx, dy = 0, 0
                    U[j][i] = dx
                    V[j][i] = dy
            
            fig = plt.Figure()
            axis = fig.add_subplot(1,1,1)
            axis.quiver(X, Y, U, V)
            
            canvas = FigureCanvas(fig)
            output = StringIO.StringIO()
            fig.savefig(output, format='png')
            output.seek(0)
            response = make_response(base64.b64encode(output.getvalue()))
            response.mimetype = 'image/png'
        except SympifyError:
            pass
    return response

if __name__ == '__main__':
    app.run(debug=True)