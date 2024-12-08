from flask import Flask, jsonify
from fileinput import filename
import pandas as pd
from flask import *
import os


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
  return jsonify({
      "Message": "app up and running successfully"
  })

@app.route("/access",methods=["POST"])
def access():
  data = request.get_json()
  name = data.get("name", "dipto")
  server = data.get("server","server1")

  message = f"User {name} received access to server {server}"

  return jsonify({
      "Message": message
  })
 

if __name__ == '__main__':
    app.run()