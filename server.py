import StringIO
import base64
import signal

import flask

from quiver.plotter import FieldPlotter

app = flask.Flask(__name__)

@app.route('/')
def quiver():
    '''Route for homepage'''
    return flask.render_template('quiver.html')

@app.route('/plot', methods=['GET',])
def plot():
    equation_string = flask.request.args.get('equation')
    diff_equation = FieldPlotter()
    diff_equation.set_equation_from_string(equation_string)
    diff_equation.make_plot()
    
    # If plotting was successful, write plot out
    if diff_equation.figure:
        
        # Write output to memory and add to response object
        output = StringIO.StringIO()
        response = flask.make_response(base64.b64encode(diff_equation.write_data(output)))
        response.mimetype = 'image/png'
        return response
    else:
        return flask.make_response('')

@app.route('/data', methods=['GET',])
def data():
    equation_string = flask.request.args.get('equation')
    plotter = FieldPlotter()
    plotter.set_equation_from_string(equation_string)
    json_data = plotter.json_data()
    response = flask.make_response(json_data)
    response.mimetype = 'text/json'
    return response

if __name__ == '__main__':
    app.run(debug=True)