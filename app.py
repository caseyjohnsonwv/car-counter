import os
from flask import Flask, redirect, session, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
#main page with statistics
def hello():
    app.config.update(SECRET_KEY = os.urandom(24))
    return "Hello, world!"

@app.route("/alive", methods=["GET"])
#simple get request to test wi-fi connectivity
def alive():
    return "Success"

@app.route("/upload-data", methods=["POST"])
#route for HTTP POST request
def upload_data():
    return "Success"
