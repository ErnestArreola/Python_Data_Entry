from flask import Flask, jsonify
from fileinput import filename
import pandas as pd
from flask import *
import os


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
      # upload file flask
        f = request.files.get('file')
 
        # Extracting uploaded file name
        data_filename = secure_filename(f.filename)
 
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],
                            data_filename))
 
        session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],data_filename)
 
        return render_template('index2.html')
    return render_template("index.html")
 

if __name__ == '__main__':
    app.run(debug=True)