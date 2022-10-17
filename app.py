from flask import Flask, render_template, request, jsonify, flash, redirect
from PIL import Image
import io
import base64
import requests

app = Flask(__name__, template_folder='templates', static_folder='static_files')
app.secret_key = "secret key_"

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'dcm'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

import torch    
import torchvision.transforms as tfms

def predict(img):
    return {
        'probablities': [.35, .81],
        'dxlist': ['pneumonia', 'abnormal XR not otherwise specified'],
        'prediction': ['abnormal XR not otherwise specified',  .81],
        'prediction_all': [
            ['pneumonia', .35], 
            ['abnormal XR not otherwise specified', .81],
        ],
    }
#
configs = {
    'appName': 'RobotCXR',
}

@app.route('/')
def hello():
    configs['title'] = f'{configs["appName"]} home'
    return render_template('index.html', configs=configs)

@app.route('/result/', methods=['GET', 'POST'])
def result():
    configs['title'] = f'{configs["appName"]} result'

    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file'] #<FileStorage: 'mpv-shot0007.jpg' ('image/jpeg')>
        print(f'[ {__file__} ]', file)

        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)

        if file and allowed_file(file.filename):

            try:
                api_url = 'http://127.0.0.1:8081/api'
                # r = requests.post(api_url, files={'file':request.files}, headers={'Content-Type':'multipart/form-data'})
                # r = requests.post(api_url, files={'file': file}, headers={'Content-Type':'multipart/form-data'})
                # r = requests.post(api_url, files={'file': 'file'}, headers={'Content-Type':'multipart/form-data'})
                # r = requests.post(api_url, files=[('file', file)], headers={'Content-Type':'multipart/form-data'})
                r = requests.post(api_url, files=[('file', file)], headers={'Content-Type':'multipart/form-data'})
                print(r)
            except Exception as e:
                # raise
                pass

            img = Image.open(file).convert('L') # PIL image
            print(f'[ {__file__} ] img size', img.size)
            sr = img.size[0]/img.size[1]
            if sr>1.5 or sr<.666:
                flash('Bad aspect ratio')
                return redirect(request.url)

            if sr >= 1: cr = img.size[1]
            else: cr = img.size[0]

            img = tfms.Compose((
                # tfms.Grayscale(),
                tfms.CenterCrop(cr),
                tfms.Resize(224),
                tfms.ToTensor(),
            ))(img).unsqueeze(0)
            print(img.shape)
            
            prediction = predict(img)
            dx, confidence = prediction['prediction']
            confidence = round(confidence*100, 2)
            configs['prediction'] = prediction

            bytesio = io.BytesIO()
            # image = image.resize((677,486))
            image = tfms.ToPILImage()(img[0])
            image.save(bytesio, format="JPEG")
            img_base64 = base64.b64encode(bytesio.getvalue()).decode('ascii')
            configs['img_base64'] = img_base64

            flash('Image successfully uploaded and displayed')
            # print(configs)
            return render_template('result.html', configs=configs)

        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif, dcm')
            return redirect(request.url)
        
    else: return render_template('index.html', configs=configs)

@app.route('/about/')
def about():
    configs['title'] = f'{configs["appName"]} about'
    return render_template('about.html', configs=configs)

@app.route('/api/')
def api():
    prediction = predict()
    return jsonify(prediction)
