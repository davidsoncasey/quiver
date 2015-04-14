import StringIO
import base64
import signal

from flask import Flask, render_template, request, make_response

from plot_equation import DiffEquation

app = Flask(__name__)

@app.route('/')
def quiver():
    '''Route for homepage'''
    return render_template('quiver.html')

@app.route('/plot/', methods=['GET',])
def plot():
    equation_string = request.args.get('equation')
    diff_equation = DiffEquation(equation_string)
    diff_equation.prep_equation()
    diff_equation.make_plot()
    
    # If plotting was successful, write plot out
    if diff_equation.figure:
        
        # Write output to memory and add to response object
        output = StringIO.StringIO()
        response = make_response(base64.b64encode(diff_equation.write_data(output)))
        response.mimetype = 'image/png'
        return response
    else:
        return make_response('')

if __name__ == '__main__':
    app.run(debug=True)