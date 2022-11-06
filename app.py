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

from predict import format_img, predict, multipart_post

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
            multipart_post(file)

            if file.filename.rsplit('.', 1)[1].lower() in ['dcm', 'dicom']:
                flash('Error: DICOM support is on the way, use other image formats for now')
                return redirect(request.url)

            else:
                img, error_msg = format_img(file)
                if error_msg:
                    flash(error_msg)
                    return redirect(request.url)


            prediction = predict(img)
            configs['prediction'] = prediction

            bytesio = io.BytesIO()
            # img.save(bytesio, format="JPEG")
            img.save(bytesio, format="PNG")
            img_base64 = base64.b64encode(bytesio.getvalue()).decode('ascii')
            configs['img_base64'] = img_base64


            print(f'[ {__file__} ]', 'Image successfully uploaded and displayed')
            return render_template('result.html', configs=configs)

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
