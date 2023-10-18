from flask import Flask, render_template,url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/temperature')
def temperature():
    return render_template('temp.html')

@app.route('/sea_levels')
def sea_levels():
    return '<h1> sea levels</h1>'

@app.route('/co2_levels')
def co2_levels():
    return render_template('co2.html')

@app.route('/air_quality')
def air_quality():
    return '<h1> air quality</h1>'

if __name__ == '__main__':
    app.run(debug=True)
