import os, db
from flask import Flask, redirect, session, request, render_template


app = Flask(__name__)
app.config.update(
    SECRET_KEY = os.environ.get("app_key", "app_key")
)


@app.route("/", methods=["GET"])
#main page with statistics
def hello():
    today = db.fetchToday()
    todayData, todayLabels = [], []
    for d,l in today:
        todayData.append(d)
        todayLabels.append(l.split('-',1)[0].strip())
    history = db.fetchHistory()
    historyData, historyLabels = [], []
    for d,l in history:
        historyData.append(d)
        historyLabels.append(l.split('-',1)[1].strip())
    data = {
    'todayData':todayData,'todayLabels':todayLabels,
    'historyData':historyData,'historyLabels':historyLabels
    }
    return render_template('index.html', data=data)


@app.route("/reset-today", methods=["GET"])
#simple get request to reset car counter
def resetToday():
    db.resetToday()
    return redirect("/")


@app.route("/reset-history", methods=["GET"])
#simple get request to reset db history
def resetHistory():
    db.resetHistory()
    return redirect("/")


@app.route("/upload-today", methods=["POST"])
#route for HTTP POST request
def upload_today():
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

    db.updateToday(car_count)
    return "Success"

@app.route("/upload-history", methods=["POST"])
#route for HTTP POST to update history
def upload_history():
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

    db.updateHistory()
    db.resetToday()
    return "Success"


if __name__ == "__main__":
    host = os.environ.get("host","127.0.0.1")
    port = os.environ.get("port", "5000")
    #db.drop_all()
    db.generate()
    app.run(host,port)
