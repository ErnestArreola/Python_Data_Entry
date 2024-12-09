from flask import Flask, jsonify
import pandas as pd
from flask import *
import os
import code
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
  return jsonify({
      "Message": "app up and running successfully"
  })


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # Check if an Excel file was uploaded
    if 'file' not in request.files:
        return {"error": "No file part in the request"}, 400
    
    file = request.files['file']
    
    # Check if the file is actually provided
    if file.filename == '':
        return {"error": "No file selected for uploading"}, 400

    # Validate the file type if necessary
    if not file.filename.endswith(('.xls', '.xlsx')):
        return {"error": "Invalid file type, only Excel files are accepted"}, 400

    result = code.main(file)

    # Return the generated Excel file
    return send_file(output, 
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     as_attachment=True,
                     download_name='result.xlsx')

 
if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=8080)