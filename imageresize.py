import os
import re
from flask import Flask,flash,request,redirect,url_for,send_from_directory,render_template
from os import walk
from werkzeug.utils import secure_filename
from PIL import Image
from resizeimage import resizeimage

UPLOAD_FOLDER = 'images' #os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app=Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

# helpers -- actual functioning components
def resize_file(in_path,out_path,size):
    with open(in_path,'r+b') as f:
        with Image.open(f) as image:
            cover=resizeimage.resize_contain(image,size)
            cover.save(out_path,image.format)

def check_img(path):
	try:
		Image.open(path)
	except IOError:
		return False
	return True

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# routes -- server part
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    
    for root,dirs,files in os.walk(UPLOAD_FOLDER):
        for file in files:
            os.remove(os.path.join(root,file))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filen=os.path.join(app.config['UPLOAD_FOLDER'],filename)
            if check_img(filen):
                resize_file(filen,filen,[2048,1152])
                return send_from_directory(app.config['UPLOAD_FOLDER'],filename,as_attachment=True)
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)