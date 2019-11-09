import os, time
from flask import Flask, redirect, session, request, render_template


app = Flask(__name__)
totalCars = 0
lastUpdate = None


@app.route("/", methods=["GET"])
#main page with statistics
def hello():
    app.config.update(SECRET_KEY = os.environ.get("app_key", "app_key"))
    if lastUpdate:
        return render_template('main.html',totalCars=totalCars,lastUpdate=lastUpdate)
    else:
        return redirect("/alive")


@app.route("/alive", methods=["GET"])
#simple get request to test wi-fi connectivity
def alive():
    return "App is live!"


@app.route("/reset", methods=["GET"])
#simple get request to reset car counter
def reset():
    global totalCars,lastUpdate
    totalCars = 0
    lastUpdate = None
    return redirect("/")


@app.route("/upload-data", methods=["POST"])
#route for HTTP POST request
def upload_data():
    try:
        request_key = request.form['upload_key']
    except Exception:
        return "ERROR: Request rejected."

    try:
        upload_key = os.environ['upload_key']
    except Exception:
        return "ERROR: Upload rejected."

    if upload_key != request_key:
        return "ERROR: Data mismatch."

    try:
        car_count = int(request.form['car_count'])
    except Exception:
        return "ERROR: Data not found."

    global totalCars, lastUpdate
    totalCars += car_count
    lastUpdate = time.strftime("%H:%M:%S - %Y-%m-%d",time.gmtime())

    return "Success"


if __name__ == "__main__":
    host = os.environ.get("host","127.0.0.1")
    port = os.environ.get("port", "5000")
    app.run(host,port)
