import os
import zipfile
from os import walk
from PIL import Image
from resizeimage import resizeimage
from flask import Flask, render_template, request,send_file
from flask_dropzone import Dropzone

basedir = os.path.abspath(os.path.dirname(__file__))

def resize_file(in_path,out_path,size):
    with open(in_path,'r') as f:
        with Image.open(f) as image:
            cover=resizeimage.resize_contain(image,size)
            cover.save(out_path,image.format)

def check_img(path):
	try:
		Image.open(path)
	except IOError:
		return False
	return True


app = Flask(__name__)

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=20,
    DROPZONE_UPLOAD_ON_CLICK=True
)

dropzone = Dropzone(app)


@app.route('/', methods=['POST', 'GET'])
def upload():
    for root,dirs,files in os.walk(app.config['UPLOADED_PATH']):
        for file in files:
            os.remove(os.path.join(root,file))
    
    if request.method == 'POST':
        for key, f in request.files.items():
            if key.startswith('file'):
                f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return render_template('index.html')

@app.route('/d')
def download():
    zipf=zipfile.ZipFile('Download.zip','w',zipfile.ZIP_DEFLATED)
    for root,dirs,files in os.walk(app.config['UPLOADED_PATH']):
        for file in files:
            filen=os.path.join(root,file)
            if check_img(filen):
                resize_file(filen,filen,[2048,1152])
                zipf.write(filen)        
    zipf.close()
    return send_file('Download.zip',
            mimetype = 'zip',
            attachment_filename= 'Download.zip',
            as_attachment = True)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
