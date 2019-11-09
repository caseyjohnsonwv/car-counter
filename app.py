import os, time
from flask import Flask, redirect, session, request, render_template


app = Flask(__name__)


@app.route("/", methods=["GET"])
#main page with statistics
def hello():
    app.config.update(SECRET_KEY = os.environ.get("app_key", "app_key"))
    if session.get("LASTUPDATE", None):
        LASTUPDATE = session["LASTUPDATE"]
        TOTALCARS = session["TOTALCARS"]
        return render_template('main.html',totalCars=TOTALCARS,lastUpdate=LASTUPDATE)
    else:
        return render_template('error.html')


@app.route("/alive", methods=["GET"])
#simple get request to test wi-fi connectivity
def alive():
    return "App is live!"


@app.route("/reset", methods=["GET"])
#simple get request to reset car counter
def reset():
    session["TOTALCARS"] = 0
    session["LASTUPDATE"] = None
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

    session["TOTALCARS"] = session.get("TOTALCARS", 0) + car_count
    session["LASTUPDATE"] = time.strftime("%H:%M:%S - %Y-%m-%d",time.gmtime())

    return "Success"


if __name__ == "__main__":
    host = os.environ.get("host","127.0.0.1")
    port = os.environ.get("port", "5000")
    app.run(host,port)
