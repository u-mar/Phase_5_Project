from flask import Flask, render_template,url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/temperature')
def temperature():
    return render_template('temp.html')

@app.route('/co2_levels')
def co2_levels():
    return render_template('co2.html')

if __name__ == '__main__':
    app.run(debug=True)
