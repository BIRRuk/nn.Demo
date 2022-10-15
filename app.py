from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates', static_folder='static_files')

def predict():
    return {
        'probablities': [.35, .81],
        'dxlist': ['pneumonia', 'abnormal XR not otherwise specified'],
        'prediction': ['abnormal XR not otherwise specified',  .81]
    }
#

@app.route('/')
def hello():
    configs = {
        'title': 'web_demo home',
    }
    return render_template('index.html', configs=configs)

@app.route('/about/')
def about():
    configs = {
        'title': 'web_demo about',
    }
    return render_template('about.html', configs=configs)

@app.route('/result/', methods=['POST'])
def result():
    configs = {
        'title': 'web_demo result page',
    }
    return render_template('result.html', configs=configs)

@app.route('/api/')
def api():
    prediction = predict()
    return jsonify(prediction)
