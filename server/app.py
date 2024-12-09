from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
import pandas as pd
from werkzeug.utils import secure_filename
from flask import *
import os
import code
import io

app = Flask(__name__)
cors = CORS(api, resources={r"/*": {"origins": "http://localhost:5173" }})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET'])
def home():
  return jsonify({
      "Message": "app up and running successfully"
  })


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400
    
    if not file.filename.endswith(('.xls', '.xlsx')):
        return {"error": "Invalid file type, only Excel files are accepted"}, 400

    # If the file is allowed, save it
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the file (e.g., read and modify the Excel file)
        df = pd.read_excel(file_path)

        # Save the modified file back
        processed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_file.xlsx')
        df.to_excel(processed_file_path, index=False)

        # Send the processed file back to the client
        return send_file(processed_file_path, as_attachment=True, download_name='processed_file.xlsx')

    return 'Invalid file format', 400
 
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)