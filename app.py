import os
import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

from image_dehazer import remove_haze

app = Flask(__name__)

# Set the path for uploading files
UPLOAD_FOLDER = 'single_image_dehazing/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set the path for saving the output image
OUTPUT_FOLDER = 'single_image_dehazing/outputImages'
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure file extensions allowed
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        # Save the uploaded file
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Read the uploaded image and apply dehazing
        HazeImg = cv2.imread(filename)
        HazeCorrectedImg, _ = remove_haze(HazeImg)

        # Save the dehazed image
        result_filename = os.path.join(app.config['OUTPUT_FOLDER'], 'result.png')
        cv2.imwrite(result_filename, HazeCorrectedImg)

        return redirect(url_for('uploaded_file', filename='result.png'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main':
    app.run(debug=True,port = 8080)
