from flask import Flask, render_template, request, jsonify, flash, redirect
import requests

app = Flask(__name__, template_folder='templates', static_folder='static_files')
app.secret_key = "secret key_"

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'dcm'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

url = 'http://127.0.0.1:8081/api'
def multipart_post(file, url=url):
    payload = {}
    files = [('file', ('', file, 'image'))]
    headers = {
      'x-api-key': 'xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx'
    }
    try:
        print(f'[ {__name__} ] uploading {files} to {url}.')
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
    except Exception as e:
        print('Exception during <multipart_post>:', e)
        response = None
    return response

configs = {
    # 'appName': 'RobotCXR',
    'appName': 'nn.Demo',
}

@app.route('/')
def hello():
    configs['title'] = f'{configs["appName"]}'
    return render_template('index.html', configs=configs)

@app.route('/result/', methods=['GET', 'POST'])
def result():

    if request.method == "POST":
        configs['title'] = f'{configs["appName"]} result'
        if 'file' not in request.files:
            flash('Error: No file uploaded')
            return redirect(request.url)

        file = request.files['file'] #<FileStorage: 'mpv-shot0007.jpg' ('image/jpeg')>
        print(f'[ {__file__} ]', file)

        if file.filename == '':
            flash('Error: No file uploaded')
            return redirect(request.url)

        if file and allowed_file(file.filename):

            if file.filename.rsplit('.', 1)[1].lower() in ['dcm', 'dicom']:
                flash('Error: DICOM support is on the way, use other image formats for now')
                return redirect(request.url)

            else:
                response = multipart_post(file)
                if response is None:
                    flash('Error: DICOM support is on the way, use other image formats for now')
                    return redirect(request.url)
                
                responsej = response.json()
                responsej['appName'] = configs['appName'] 
                responsej['title'] = configs['title'] 

            print(f'[ {__file__} ]', 'Image successfully uploaded and displayed')
            if responsej['exit_code'] == 0:
                return render_template('result.html', configs=responsej)
            else:
                flash(responsej['error_msg'])
                return redirect(request.url)

        else:
            flash(f'Error: Allowed file types are: {ALLOWED_EXTENSIONS}')
            return redirect(request.url)
        
    else:
        configs['title'] = f'{configs["appName"]}'
        return render_template('index.html', configs=configs)

@app.route('/about/')
def about():
    configs['title'] = f'{configs["appName"]} about'
    return render_template('about.html', configs=configs)

@app.route('/api/')
def api():
    prediction = predict()
    return jsonify(prediction)
