from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def quiver():
    return render_template('quiver.html')

@app.route('/plot/', methods=['GET', 'POST'])
def plot():
    equation = request.args.get('equation')
    return render_template('plot.html', equation=equation)

if __name__ == '__main__':
    app.run(debug=True)