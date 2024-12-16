from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
import pandas as pd
from werkzeug.utils import secure_filename
from flask import *
import os
from process import main
import io
from fileinput import filename

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit upload size to 16MB

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
    file.save(file.filename)

    if file.filename == '':
        return 'No selected file', 400
    
    if not file.filename.endswith(('.xlsx')):
        return {"error": "Invalid file type, only Excel files are accepted"}, 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

    # df = pd.read_excel(file, engine='openpyxl')


    # If the file is allowed, save it

    # Process the file (e.g., read and modify the Excel file)

    processed_file = main(file)
    processed_file.to_excel("Output.xlsx")

    
    return send_file('Output.xlsx', 
            mimetype='application/vnd.ms-excel',
            as_attachment=True,
            download_name = 'Complete.xlsx'
        )

    # else:
    #     return send_file(filepath, as_attachment=True)
    # return send_file(processed_file, 
    #                  mimetype='application/vnd.ms-excel',
    #                  as_attachment=True,
    #                  download_name = 'processed.xlsx'
    #                  )
 
if __name__ == '__main__':
    # app.run()
    app.run(debug=True, host="0.0.0.0", port=8080)
