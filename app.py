import os, db
from flask import Flask, redirect, session, request, render_template


app = Flask(__name__)
app.config.update(
    SECRET_KEY = os.environ.get("app_key", "app_key")
)


@app.route("/", methods=["GET"])
#main page with statistics
def hello():
    data = db.fetch()
    if data:
        id, TOTALCARS, LASTUPDATE = data
        return render_template('main.html',totalCars=TOTALCARS,lastUpdate=LASTUPDATE)
    else:
        return render_template('error.html')


@app.route("/reset", methods=["GET"])
#simple get request to reset car counter
def reset():
    db.reset()
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

    TOTALCARS = session.get("TOTALCARS", 0) + car_count
    db.update(TOTALCARS)

    return "Success"


if __name__ == "__main__":
    host = os.environ.get("host","127.0.0.1")
    port = os.environ.get("port", "5000")
    db.generate()
    app.run(host,port)
