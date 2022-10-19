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

def predict(img):
    # img = tfms.Grayscale()(img)
    # img = tfms.ToTensor()(img)
    # img = img.unsqueeze(0)

    return {
        # 'probablities': [.35, .914],
        # 'dxlist': ['pneumonia', 'abnormal XR not otherwise specified'],
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
                try:
                    img = Image.open(file).convert('L') # PIL image
                except Exception as e:
                    flash(f'Error: Your file {file.filename} could not be opended.')
                    return redirect(request.url)
                    # raise e

                im_sze = img.size
                print(f'[ {__file__} ] img size', im_sze)

                aspect = im_sze[0]/im_sze[1]
                if aspect>1.5 or aspect<.666:
                    flash(f'Error: Bad aspect ratio aspect ratio {im_sze}, {round(aspect,3)}x')
                    return redirect(request.url)

                sz_min = min(im_sze)
                if sz_min < 224:
                    flash(f'Error: Image dimenssions size too small {im_sze}')
                    return redirect(request.url)

                crop_x = (im_sze[0]-sz_min)//2
                crop_y = (im_sze[1]-sz_min)//2

                img = img.crop(box=(crop_x, crop_y, crop_x+sz_min, crop_y+sz_min))
                img = img.resize((224,224))

    
            prediction = predict(img)
            configs['prediction'] = prediction

            bytesio = io.BytesIO()
            img.save(bytesio, format="JPEG")
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
